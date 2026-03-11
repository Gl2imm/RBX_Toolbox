import requests
import json
from RBX_Toolbox import glob_vars


### Debug prints
DEBUG = False
dprint = lambda *args, **kwargs: print(*args, **kwargs) if DEBUG else None

### Get Data from Assetdelivery API
def get_asset_data(rbx_asset_id, headers, RobloxAssetFormat:str = None):
	asset_data = None
	rbx_imp_error = None
	glob_vars.rbx_imp_error = None
	if RobloxAssetFormat:
		local_headers = headers.copy() 
		local_headers["Roblox-AssetFormat"] = RobloxAssetFormat
	url = f"https://apis.roblox.com/asset-delivery-api/v1/assetId/{rbx_asset_id}"
	dprint("Downloading Asset:")
	dprint("url: ", url)
	try:
		response = requests.get(url, headers=local_headers if RobloxAssetFormat else headers)
	except:     
		rbx_imp_error = "Error Connecting to Assetdelivery API"
		glob_vars.rbx_imp_error = rbx_imp_error
	else:
		if response.status_code == 200:
			json_data = json.loads(response.content)
			dprint("Asset json_data: " , json_data)
			asset_url = json_data.get("location")
			if asset_url:
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
		elif response.status_code == 401:
			rbx_imp_error = f"{response.status_code}: Access Denied"
			glob_vars.rbx_imp_error = rbx_imp_error
		elif response.status_code == 404:
			rbx_imp_error = f"{response.status_code}: Asset Not Found"
			glob_vars.rbx_imp_error = rbx_imp_error    
		else:
			rbx_imp_error = f"{response.status_code}: Error getting Asset Data URL"
			glob_vars.rbx_imp_error = rbx_imp_error  
	dprint("rbx_imp_error: ", rbx_imp_error)
	dprint("")   
	return asset_data, rbx_imp_error