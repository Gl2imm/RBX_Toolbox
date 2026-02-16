import requests
import json
from RBX_Toolbox import glob_vars


### Debug prints
DEBUG = True
dprint = lambda *args, **kwargs: print(*args, **kwargs) if DEBUG else None

### Get Data from Assetdelivery API
def get_asset_data(rbx_asset_id, headers, RobloxAssetFormat:str = None):
	asset_data = None
	rbx_imp_error = None
	glob_vars.rbx_imp_error = None
	
	# 1. Primary API (apis.roblox.com)
	# User request (Step 787): Implement logic from backup
	# Backup uses Primary API WITH the header.
	primary_headers = headers.copy()
	if RobloxAssetFormat:
		primary_headers["Roblox-AssetFormat"] = RobloxAssetFormat
		
	url = f"https://apis.roblox.com/asset-delivery-api/v1/assetId/{rbx_asset_id}"
	dprint("Downloading Asset (Primary v1):")
	dprint("url: ", url)
	
	try:
		response = requests.get(url, headers=primary_headers)
	except:     
		rbx_imp_error = "Error Connecting to Assetdelivery API"
		glob_vars.rbx_imp_error = rbx_imp_error
		response = None
	
	perform_fallback = False
	if response:
		if response.status_code == 200:
			try:
				json_data = json.loads(response.content)
				dprint("Asset json_data: " , json_data)
				
				# Check for soft errors (API returns 200 but JSON says error)
				if "errors" in json_data or not json_data.get("location"):
					dprint("Soft error detected in JSON response.")
					perform_fallback = True
				else:
					asset_url = json_data.get("location")
					try:
						asset_response = requests.get(asset_url)
					except:     
						rbx_imp_error = "Error Connecting to Auth Asset Data URL"
						glob_vars.rbx_imp_error = rbx_imp_error
					else:
						if asset_response.status_code == 200:
							asset_data = asset_response.content
						else:
							rbx_imp_error = f"{response.status_code}: Error getting Asset Data"
							glob_vars.rbx_imp_error = rbx_imp_error
			except Exception as e:
				dprint(f"Error parsing JSON: {e}")
				perform_fallback = True
		elif response.status_code == 404:
			perform_fallback = True
		elif response.status_code == 401:
			rbx_imp_error = f"{response.status_code}: Access Denied"
			glob_vars.rbx_imp_error = rbx_imp_error
		else:
			rbx_imp_error = f"{response.status_code}: Error getting Asset Data URL"
			glob_vars.rbx_imp_error = rbx_imp_error
	else:
		perform_fallback = True

	# 2. Fallback Logic (Legacy API Chain)
	if perform_fallback:
		dprint(f"Primary API failed for {rbx_asset_id}. Trying legacy endpoints...")
		
		# Prepare headers for legacy
		legacy_headers = headers.copy()
		
		# Define endpoints chain (Only V2 as requested)
		endpoints = []
		endpoints.append((f"https://assetdelivery.roblox.com/v2/asset/?id={rbx_asset_id}", bool(RobloxAssetFormat), "Legacy v2"))

		for url, use_format_header, label in endpoints:
			dprint(f"Attempting {label}: {url}")
			try:
				current_headers = legacy_headers.copy()
				if use_format_header and RobloxAssetFormat:
					current_headers["Roblox-AssetFormat"] = RobloxAssetFormat
				
				res = requests.get(url, headers=current_headers)
				
				if res.status_code == 200:
					# Strict V2 JSON Parsing
					try:
						j_data = json.loads(res.content)
						loc_url = None
						
						# Check for errors in JSON
						if "errors" in j_data:
							dprint(f"{label} JSON Error: {j_data['errors']}")
							continue # Treat as failed attempt
							
						# Check for location(s)
						if "locations" in j_data and j_data["locations"]:
							loc_url = j_data["locations"][0].get("location")
						elif "location" in j_data:
							loc_url = j_data.get("location")
						
						if loc_url:
							dprint(f"{label} found redirect ID: {loc_url}")
							res_file = requests.get(loc_url)
							if res_file.status_code == 200:
								dprint(f"{label} Success!")
								asset_data = res_file.content
								rbx_imp_error = None
								glob_vars.rbx_imp_error = None
								return asset_data, None
					except Exception as e:
						dprint(f"{label} JSON/Download Error: {e}")
						continue
							
				dprint(f"{label} failed: {res.status_code}")
				
			except Exception as e:
				dprint(f"{label} error: {e}")
				continue
				
		# If loop finishes without return, all failed
		if not rbx_imp_error:
			rbx_imp_error = "Asset Not Found (All Endpoints)"
		glob_vars.rbx_imp_error = rbx_imp_error

	dprint("rbx_imp_error: ", rbx_imp_error)
	dprint("")   
	return asset_data, rbx_imp_error