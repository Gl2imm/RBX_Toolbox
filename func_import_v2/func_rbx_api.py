import requests
from RBX_Toolbox import glob_vars
import time




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
		data = requests.get(url)
	except Exception as e:     
		rbx_imp_error = f"Error Getting Catalog Bundle Data: {str(e)}"
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
		response = requests.get(url)
	except Exception as e:
		rbx_imp_error = f"Connection Error: {str(e)}"
		return None, None, None, rbx_imp_error
		
	print(f"DEBUG ASSET DATA - Status: {response.status_code}, Body: {response.text}")
	if response.status_code == 200:
		data = response.json()
		rbx_asset_name = data.get("name")
		rbx_asset_type_id = data.get("assetType")
		rbx_asset_creator = data.get("creatorName")
		
		return rbx_asset_name, rbx_asset_type_id, rbx_asset_creator, None
	else:
		if response.status_code in [404, 400]:
			# Fallback: Economy API (handles Store Models, Classic Clothes, etc.)
			eco_url = f"https://economy.roblox.com/v2/assets/{rbx_asset_id}/details"
			try:
				eco_response = requests.get(eco_url)
				print(f"DEBUG ECONOMY API - Status: {eco_response.status_code}, Body: {eco_response.text[:500]}")
				if eco_response.status_code == 200:
					eco_data = eco_response.json()
					rbx_asset_name = eco_data.get("Name")
					rbx_asset_type_id = eco_data.get("AssetTypeId")
					creator_data = eco_data.get("Creator", {})
					rbx_asset_creator = creator_data.get("Name")
					return rbx_asset_name, rbx_asset_type_id, rbx_asset_creator, None
				else:
					print(f"DEBUG ECONOMY API failed with {eco_response.status_code}")
			except Exception as eco_e:
				print(f"DEBUG ECONOMY API exception: {eco_e}")
			rbx_imp_error = f"{response.status_code}: Invalid Asset ID"
		else:
			rbx_imp_error = f"Error {response.status_code} fetching asset details"
			
	return None, None, None, rbx_imp_error





### check Thumbnail API state (often not ready yet)
def check_thumbnail_api_state(url, itm_type:str, max_retries=3, delay=1.0):
	"""Retries until the avatar state is 'Completed' or 'Blocked'. itm_type - Avatar or Accessory. Returns (data, rbx_char_error, rbx_asset_error)."""
	is_asset = True if itm_type == "Accessory" else False
	is_avatar = True if itm_type == "Avatar" else False
	data = None
	error = None
	
	# In V2 we mainly use rbx_imp_error or return error string, but for compatibility let's keep local error var
	
	for attempt in range(max_retries):
		try:
			response = requests.get(url)
		except Exception as e:
			error = f"Thumbnail api check exception: {e}"
			return data, error

		if response.status_code != 200:
			error = f"{response.status_code}: Error contacting thumbnail API"
			return data, error

		data = response.json()
		state = data.get("state") or data.get("data", [{}])[0].get("state")

		if state == "Completed":
			return data, None
		
		elif state == "Blocked":
			if is_asset:
				error = "Thumbnail API: Banned Item - unable to get image"
			else:
				error = "Thumbnail API: Banned User - unable to get image"
			return data, error

		#print(f"Thumbnail API returning state: {state}. Retrying... Attempt {attempt+1} of {max_retries}")
		time.sleep(delay)

	error = f"Thumbnail API did not return 'Completed' state after {max_retries} retries"
	return data, error


### Get Accessory Preview Image URL
def get_asset_and_bundle_img_url(rbx_asset_id, rbx_is_bundle):
	rbx_size = '150x150'
	rbx_format = 'Png'
	rbx_isCircular = 'false'
	if rbx_is_bundle:
		url = f"https://thumbnails.roblox.com/v1/bundles/thumbnails?bundleIds={rbx_asset_id}&size={rbx_size}&format={rbx_format}&isCircular={rbx_isCircular}"
	else:
		url = f"https://thumbnails.roblox.com/v1/assets?assetIds={rbx_asset_id}&returnPolicy=PlaceHolder&size={rbx_size}&format={rbx_format}&isCircular={rbx_isCircular}" 
	
	data, rbx_asset_error = check_thumbnail_api_state(url, "Accessory")
	rbx_asset_img_url = None
	
	if rbx_asset_error == None:
		rbx_asset_img_url = data.get("imageUrl") or data.get("data", [{}])[0].get("imageUrl")
		
	return rbx_asset_img_url, rbx_asset_error


### Get Accessory Preview Image
def get_asset_and_bundle_img(rbx_asset_img_url):
	rbx_asset_error = None
	image_data = None
	
	try:
		response = requests.get(rbx_asset_img_url)
		if response.status_code == 200:
			image_data = response.content
		else:
			rbx_asset_error = f"{response.status_code}: Error getting Thumbnail IMG"
	except Exception as e:
		rbx_asset_error = f"Error downloading thumbnail: {str(e)}"
		
	return image_data, rbx_asset_error
