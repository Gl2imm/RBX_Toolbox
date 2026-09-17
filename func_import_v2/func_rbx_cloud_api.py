import requests
import json
import time
from .. import glob_vars


### Debug prints
DEBUG = False
dprint = lambda *args, **kwargs: print(*args, **kwargs) if DEBUG else None


# ─────────────────────────────────────────────
#  Asset readiness
#
#  The asset-delivery API answers 200 even when it cannot hand the asset over:
#  "location" is then absent and "errors" says why. The case that matters here is
#  CustomErrorCode 21 (AssetContentRepresentationGenerating) — Roblox is still
#  building that representation (a freshly uploaded texture, or the
#  avatar_meshpart_accessory build of an item), so the download link simply is
#  not ready yet and the very same request succeeds a moment later.
#
#  Without this, a not-ready asset looks identical to a hard failure: the caller
#  gets no data, and for textures rbx_import_textures silently drops the map —
#  which is how a ColorMap can go missing from an otherwise successful import and
#  then appear on a re-import.
#
#  Only codes worth waiting on are retried, so a genuinely missing or blocked
#  asset still fails fast instead of stalling the import.
# ─────────────────────────────────────────────

#: Error codes that mean "ask again shortly", from
#: Roblox.Web.Assets.IAssetItemError.CustomErrorCode.
RETRYABLE_ASSET_ERROR_CODES = {
	21,  # AssetContentRepresentationGenerating - still being generated
	2,   # AssetPermissionCheckFailed - the check errored, not a denial
	4,   # AgeRecommendationCheckFailed - as above
}

#: HTTP statuses worth retrying on either the delivery API or the CDN.
RETRYABLE_HTTP_STATUS = {408, 425, 429, 500, 502, 503, 504}

ASSET_READY_ATTEMPTS = 3    # total tries, including the first
ASSET_READY_DELAY    = 1.0  # seconds; multiplied by the attempt number
REQUEST_TIMEOUT      = 60   # seconds


def _asset_error_codes(json_data):
	"""Collect numeric error codes from an asset-delivery payload.

	The schema names the field "CustomErrorCode", but live responses carry a
	lowercase "code"/"message" pair, so both spellings are read.
	"""
	codes = []
	for err in (json_data.get("errors") or []):
		if not isinstance(err, dict):
			continue
		for key in ("CustomErrorCode", "customErrorCode", "Code", "code"):
			value = err.get(key)
			if isinstance(value, int):
				codes.append(value)
	return codes


def _asset_is_pending(json_data):
	"""True when a location-less 200 means "not ready yet" rather than "no"."""
	codes = _asset_error_codes(json_data)
	if not codes:
		# 200 with neither a location nor an explanation - treat as transient.
		return True
	return any(code in RETRYABLE_ASSET_ERROR_CODES for code in codes)


### Get Data from Assetdelivery API
def get_asset_data(rbx_asset_id, headers, RobloxAssetFormat:str = None, max_attempts:int = ASSET_READY_ATTEMPTS):
	"""Download an asset, re-querying while it reports as still being generated.

	Returns (asset_data, rbx_imp_error) exactly as before.
	"""
	asset_data = None
	rbx_imp_error = None
	glob_vars.rbx_imp_error = None
	if RobloxAssetFormat:
		local_headers = headers.copy()
		local_headers["Roblox-AssetFormat"] = RobloxAssetFormat
	req_headers = local_headers if RobloxAssetFormat else headers
	url = f"https://apis.roblox.com/asset-delivery-api/v1/assetId/{rbx_asset_id}"
	dprint("Downloading Asset:")
	dprint("url: ", url)

	for attempt in range(1, max_attempts + 1):
		# Reset per attempt so a success after a retry reports no error.
		asset_data = None
		rbx_imp_error = None
		should_retry = False

		try:
			response = requests.get(url, headers=req_headers, timeout=REQUEST_TIMEOUT)
		except Exception as e:
			rbx_imp_error = "Error Connecting to Assetdelivery API"
			should_retry = True
			dprint(f"  attempt {attempt}: {e}")
		else:
			if response.status_code == 200:
				json_data = json.loads(response.content)
				dprint("Asset json_data: " , json_data)
				asset_url = json_data.get("location")
				if asset_url:
					try:
						asset_response = requests.get(asset_url, timeout=REQUEST_TIMEOUT)
					except Exception as e:
						rbx_imp_error = "Error Connecting to Auth Asset Data URL"
						should_retry = True
						dprint(f"  attempt {attempt}: {e}")
					else:
						if asset_response.status_code == 200:
							asset_data = asset_response.content
						else:
							# Report the CDN's status, not the delivery API's.
							rbx_imp_error = f"{asset_response.status_code}: Error getting Asset Data"
							should_retry = asset_response.status_code in RETRYABLE_HTTP_STATUS
				else:
					# 200 but no download link: either still generating, or refused.
					if _asset_is_pending(json_data):
						rbx_imp_error = f"Asset {rbx_asset_id} is not ready yet"
						should_retry = True
					else:
						rbx_imp_error = f"Error getting Asset Data URL: {json_data.get('errors')}"
			elif response.status_code == 401:
				rbx_imp_error = f"{response.status_code}: Access Denied"
			elif response.status_code == 404:
				rbx_imp_error = f"{response.status_code}: Asset Not Found"
			else:
				rbx_imp_error = f"{response.status_code}: Error getting Asset Data URL"
				should_retry = response.status_code in RETRYABLE_HTTP_STATUS

		if asset_data is not None or not should_retry or attempt == max_attempts:
			break

		dprint(f"  {rbx_imp_error} - retrying ({attempt}/{max_attempts - 1})")
		time.sleep(ASSET_READY_DELAY * attempt)

	if rbx_imp_error:
		glob_vars.rbx_imp_error = rbx_imp_error
	dprint("rbx_imp_error: ", rbx_imp_error)
	dprint("")
	return asset_data, rbx_imp_error