import requests
from RBX_Toolbox import glob_vars



######################################
##### Bundles Specific functions #####
######################################

### Get Catalog information for Bundles
def get_catalog_bundle_data(rbx_asset_id, headers):
	rbx_bundledItems = None
	rbx_asset_name = None
	rbx_asset_type_id = None
	rbx_asset_creator = None
	rbx_imp_error = None
	glob_vars.rbx_asset_error = None
	url = f"https://catalog.roblox.com/v1/catalog/items/{rbx_asset_id}/details?itemType=Bundle"
	try:
		data = requests.get(url, headers=headers)
	except:     
		rbx_imp_error = "Error Getting Catalog Bundle Data"
		glob_vars.rbx_imp_error = rbx_imp_error
	else:
		if data.status_code == 200:
			data = data.json()
			rbx_bundledItems = data["bundledItems"] # will get list of dictionaries with items
			rbx_asset_name = data["name"]
			rbx_asset_type_id = data["bundleType"] 
			rbx_asset_creator = data["creatorName"]
		else:
			if data.status_code == 404:
				rbx_imp_error = f"{data.status_code}: Invalid Bundle ID"
			else:
				rbx_imp_error = f"{data.status_code}: Error getting Catalog Bundle Data"
			glob_vars.rbx_imp_error = rbx_imp_error   
	return rbx_asset_name, rbx_asset_type_id, rbx_asset_creator, rbx_bundledItems, rbx_imp_error



# Get information for a single asset (not bundle)
def get_catalog_asset_data(rbx_asset_id, headers):
	# Using Catalog API endpoint to get asset details (matches rbx_import.py logic)
	url = f"https://catalog.roblox.com/v1/catalog/items/{rbx_asset_id}/details?itemType=Asset"
	
	rbx_asset_name = None
	rbx_asset_type_id = None
	rbx_asset_creator = None
	rbx_imp_error = None
	
	try:
		response = requests.get(url, headers=headers)
	except Exception as e:
		rbx_imp_error = f"Connection Error: {str(e)}"
		return None, None, None, null, rbx_imp_error # Match return signature of get_catalog_bundle_data partialy? No, existing usage expecting 4 values.
		# specific usage in rbx_import_discovery: asset_name, asset_type_id, asset_creator, asset_error = ...
		return None, None, None, rbx_imp_error
		
	if response.status_code == 200:
		data = response.json()
		rbx_asset_name = data.get("name")
		rbx_asset_type_id = data.get("assetType")
		rbx_asset_creator = data.get("creatorName")
		
		return rbx_asset_name, rbx_asset_type_id, rbx_asset_creator, None
	else:
		if response.status_code == 404:
			# Not an asset or invalid ID
			pass
		else:
			rbx_imp_error = f"Error {response.status_code} fetching asset details"
			
	return None, None, None, rbx_imp_error