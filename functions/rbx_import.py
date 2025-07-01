import bpy
import os
import requests
from bpy_extras.object_utils import AddObjectHelper
from RBX_Toolbox import glob_vars
from glob_vars import addon_path
import asyncio
import time
import re
import json


### Debug prints
DEBUG = False
dprint = lambda *args, **kwargs: print(*args, **kwargs) if DEBUG else None

## Remove restricted characters from string ##
def replace_restricted_char(str: str = None):
    '''Replace restricted characters in string with underscores'''
    if str is None:
        return
    restricted_chars = '\/*?:"<>|.,'
    replace_map = dict((ord(char), '_') for char in restricted_chars)
    new_str = str.translate(replace_map)
    return new_str


# This asynchronous method is invoked as a separate coroutine from the main thread
async def renew_token(context):
    """Refreshes Auth Token"""
    from oauth.lib.oauth2_client import RbxOAuth2Client
    window_manager = context.window_manager
    rbx = window_manager.rbx
    oauth2_client = RbxOAuth2Client(rbx)
    await oauth2_client.refresh_login_if_needed()
    access_token = oauth2_client.token_data["access_token"]
    dprint("Auth Token refresh after: " , oauth2_client.token_data["refresh_after"])
    return access_token
    

### Get CDN URL
def get_cdn_url(hash):
    i = 31
    for char in hash:
        i ^= ord(char)
    return f"https://t{i%8}.rbxcdn.com/{hash}"


### Download files
def download(url, itm_type, asset_or_ava):
    """Download files. itm_type - Avatar or Accessory."""
    is_asset = True if asset_or_ava == "Accessory" else False
    is_avatar = True if asset_or_ava == "Avatar" else False
    data = None
    if is_asset:
        rbx_asset_error = None
        data = requests.get(url) 
        if data.status_code == 200:
            data = data.content
        else:
            rbx_asset_error = f"{data.status_code}: Error downloading {itm_type} file"
            glob_vars.rbx_asset_error = rbx_asset_error
        return data, rbx_asset_error
    if is_avatar:
        rbx_char_error = None
        data = requests.get(url) 
        if data.status_code == 200:
            data = data.content
        else:
            rbx_char_error = f"{data.status_code}: Error downloading {itm_type} file"
            glob_vars.rbx_char_error = rbx_char_error
        return data, rbx_char_error


### Save Downloaded files
def save_to_file(file, data, itm_type, asset_or_ava):
    """Saving files. itm_type - Avatar or Accessory."""
    is_asset = True if asset_or_ava == "Accessory" else False
    is_avatar = True if asset_or_ava == "Avatar" else False
    if is_asset:
        rbx_asset_error = None
        try:
            with open(file, "wb") as f:
                f.write(data) 
        except:
            rbx_asset_error = f"Error saving {itm_type}"
            glob_vars.rbx_asset_error = rbx_asset_error
    if is_avatar:
        rbx_char_error = None
        try:
            with open(file, "wb") as f:
                f.write(data) 
        except:
            rbx_char_error = f"Error saving {itm_type}"
            glob_vars.rbx_char_error = rbx_char_error



##### Convert username input #####
def check_username_field_and_extract_id(rbx_username_entered):
    username_field_is = None
    rbx_char_error = None
    if "https://www.roblox.com/" in rbx_username_entered:
        rbx_username_or_id = rbx_username_entered.lstrip("https://www.roblox.com/users/")
        rbx_username_or_id = rbx_username_or_id.split("/")[0]
        username_field_is = "id"
        if not rbx_username_or_id.isdigit():
            rbx_char_error = "Error: Invalid profile URL"  
            glob_vars.rbx_char_error = rbx_char_error         
    elif rbx_username_entered.isdigit():
        rbx_username_or_id = rbx_username_entered
        username_field_is = "id"
    else:
        rbx_username_or_id = rbx_username_entered
        username_field_is = "username"
    return rbx_username_or_id, username_field_is, rbx_char_error



##### Create Folders #####
def create_folders(rbx_char, addon_path):
    if rbx_char == 'folder_character':
        rbx_imported_char_path = os.path.join(addon_path, glob_vars.rbx_import_main_folder, glob_vars.rbx_imported_char_fldr)
        if not os.path.exists(rbx_imported_char_path):
            os.makedirs(rbx_imported_char_path)
        os.startfile(os.path.dirname(rbx_imported_char_path))
    if rbx_char == 'folder_accessory':
        rbx_imported_acc_path = os.path.join(addon_path, glob_vars.rbx_import_main_folder, glob_vars.rbx_imported_acc_fldr)
        if not os.path.exists(rbx_imported_acc_path):
            os.makedirs(rbx_imported_acc_path)
        os.startfile(os.path.dirname(rbx_imported_acc_path))  



### Get User ID from Username
def get_user_id(rbx_user_name, headers):
    rbx_user_id = None
    rbx_char_error = None
    glob_vars.rbx_char_error = None
    glob_vars.rbx_user_name = rbx_user_name
    payload = {
                "usernames": [rbx_user_name],
                "excludeBannedUsers" : 'true'
                }
    try:
        data = requests.post("https://users.roblox.com/v1/usernames/users", json=payload, headers=headers)
    except:
        rbx_char_error = "Get User ID Error, no respose"
        glob_vars.rbx_char_error = rbx_char_error
    else:
        if data.status_code == 200:
            data = data.json()
            try:
                rbx_user_id = data.get('data')[0]['id']
            except:
                rbx_char_error = "Error: Unable to find this user" 
                glob_vars.rbx_char_error = rbx_char_error       
        else:
            rbx_char_error = f"{data.status_code}: Error getting User ID"
            glob_vars.rbx_char_error = rbx_char_error   
    return rbx_user_id, rbx_char_error



### Get Username from user ID
def get_user_name(rbx_user_id, headers):
    rbx_user_name = None
    rbx_char_error = None
    glob_vars.rbx_user_name = None
    glob_vars.rbx_char_error = None
    try:
        data = requests.get(f"https://users.roblox.com/v1/users/{rbx_user_id}", headers=headers)
    except:
        rbx_char_error = "Get User Name Error, no respose"
        glob_vars.rbx_char_error = rbx_char_error   
    else: 
        if data.status_code == 200:
            data = data.json()
            rbx_user_name = data['name']
            glob_vars.rbx_user_name = rbx_user_name
        else:
            rbx_char_error = f"{data.status_code}: Error getting User Name" 
            glob_vars.rbx_char_error = rbx_char_error   
    return rbx_user_name, rbx_char_error



### check Thumbnail API state (often not ready yet)
def check_thumbnail_api_state(url, itm_type:str, max_retries=3, delay=1.0):
    """Retries until the avatar state is 'Completed' or 'Blocked'. itm_type - Avatar or Accessory. Returns (data, rbx_char_error, rbx_asset_error)."""
    is_asset = True if itm_type == "Accessory" else False
    is_avatar = True if itm_type == "Avatar" else False
    data = None
    error = None
    if is_asset:
        glob_vars.rbx_asset_error = None 
    else:
        glob_vars.rbx_char_error = None 
    for attempt in range(max_retries):
        try:
            response = requests.get(url)
        except Exception as e:
            error = f"Thumbnail api check exception: {e}"
            if is_asset:
                glob_vars.rbx_asset_error = error
            else:
                glob_vars.rbx_char_error = error
            return data, error

        if response.status_code != 200:
            error = f"{response.status_code}: Error contacting thumbnail API"
            if is_asset:
                glob_vars.rbx_asset_error = error
            else:
                glob_vars.rbx_char_error = error
            return data, error

        data = response.json()
        state = data.get("state") or data.get("data", [{}])[0].get("state")

        if state == "Completed":
            return data, error
        
        elif state == "Blocked":
            if is_asset:
                error = "Thumbnail API: Banned Item - unable to get image"
            else:
                error = "Thumbnail API: Banned User - unable to get image"
                if is_asset:
                    glob_vars.rbx_asset_error = error
                else:
                    glob_vars.rbx_char_error = error
                return data, error
        print(f"Thumbnail API returning state: {data.get('state') or data.get('data', [{}])[0].get('state')}. Retrying... Attempt {attempt+1} of {max_retries}")
        time.sleep(delay)

    error = f"Thumbnail API did not return 'Completed' state after {max_retries} retries"
    if is_asset:
        glob_vars.rbx_asset_error = error
    else:
        glob_vars.rbx_char_error = error
    return data, error



### Get User Avatar
def get_user_avatar_url(rbx_user_id):
    rbx_usr_img_url = None
    rbx_char_error = None
    glob_vars.rbx_char_error = None 
    rbx_size = '250x250'
    rbx_format = 'Png'
    rbx_isCircular = 'false'                                            
    url = f"https://thumbnails.roblox.com/v1/users/avatar?userIds={rbx_user_id}&size={rbx_size}&format={rbx_format}&isCircular={rbx_isCircular}"
    data, rbx_char_error = check_thumbnail_api_state(url, "Avatar")
    if rbx_char_error == None:
        rbx_usr_img_url = data.get("imageUrl") or data.get("data", [{}])[0].get("imageUrl")
        #rbx_usr_img_url = data["data"][0]["imageUrl"]
    return rbx_usr_img_url, rbx_char_error


### Get User Avatar Image
def get_user_avatar_img(rbx_usr_img_url):
    rbx_char_error = None
    glob_vars.rbx_char_error = None 
    image_data = requests.get(rbx_usr_img_url)
    if image_data.status_code == 200:
        image_data = image_data.content
    else:
        rbx_char_error = f"{image_data.status_code}: Error getting Avatar IMG"
        glob_vars.rbx_char_error = rbx_char_error   
    return image_data, rbx_char_error

    
### Get User Avatar Hashes Links
def get_user_hashes(rbx_user_id): 
    rbx_char_error = None
    rbx_usr_hsh_urls = None
    glob_vars.rbx_char_error = None
    url = f"https://thumbnails.roblox.com/v1/users/avatar-3d?userId={rbx_user_id}"
    data, rbx_char_error = check_thumbnail_api_state(url, "Avatar")                  
    if rbx_char_error == None:
        rbx_usr_hsh_urls = data.get("imageUrl") or data.get("data", [{}])[0].get("imageUrl") #Get Link to OBJ and Textures Hashes
        #rbx_usr_hsh_urls = data["data"][0]["imageUrl"] #Get Link to OBJ and Textures Hashes
        rbx_usr_hsh_urls = requests.get(rbx_usr_hsh_urls)
        if rbx_usr_hsh_urls.status_code == 200:
            rbx_usr_hsh_urls = rbx_usr_hsh_urls.json() #Get OBJ and Textures Hashes links
        else:
            rbx_char_error = f"{rbx_usr_hsh_urls.status_code}: Error getting user hashes"
            glob_vars.rbx_char_error = rbx_char_error 
    return rbx_usr_hsh_urls, rbx_char_error


##### Extract Accessory ID from user input #####
def check_accessory_field_and_extract_id(rbx_accessory_entered):
    rbx_cat_url = "https://www.roblox.com/catalog/"
    rbx_bndl_url = "https://www.roblox.com/bundles/"
    rbx_asset_id = None
    rbx_asset_error = None
    glob_vars.rbx_asset_error = None
    rbx_is_bundle = False
    glob_vars.rbx_is_bundle = rbx_is_bundle
    if not rbx_accessory_entered.isdigit() and rbx_cat_url not in rbx_accessory_entered and rbx_bndl_url not in rbx_accessory_entered:
        rbx_asset_error = "Only ID or Marketplace link supported"
        glob_vars.rbx_asset_error = rbx_asset_error
    elif rbx_cat_url in rbx_accessory_entered:
        rbx_asset_id = rbx_accessory_entered.lstrip(rbx_cat_url)
        rbx_asset_id = rbx_asset_id.split("/")[0]
    elif rbx_bndl_url in rbx_accessory_entered:
        rbx_asset_id = rbx_accessory_entered.lstrip(rbx_bndl_url)
        rbx_asset_id = rbx_asset_id.split("/")[0]
        rbx_is_bundle = True
        glob_vars.rbx_is_bundle = rbx_is_bundle
    else:
        rbx_asset_id = rbx_accessory_entered
    return rbx_asset_id, rbx_is_bundle, rbx_asset_error












### Get Catalog information for Assets
def get_catalog_asset_data(rbx_asset_id, headers, rbx_char):
    rbx_asset_name, rbx_asset_type_id, rbx_asset_creator = None, None, None
    rbx_asset_error = None
    glob_vars.rbx_asset_error = None
    url = f"https://catalog.roblox.com/v1/catalog/items/{rbx_asset_id}/details?itemType=Asset"
    try:
        data = requests.get(url, headers=headers)
    except:     
        rbx_asset_error = "Error Getting Catalog Asset Data"
        glob_vars.rbx_asset_error = rbx_asset_error
    else:
        if data.status_code == 200:
            data = data.json()
            rbx_asset_name = data['name']
            rbx_asset_type_id = data['assetType']
            rbx_asset_creator = data['creatorName']
            if rbx_char == 'preview_accessory':
                glob_vars.rbx_asset_name = rbx_asset_name
                glob_vars.rbx_asset_creator = rbx_asset_creator
        else:
            if data.status_code == 400:
                rbx_asset_error = f"{data.status_code}: Invalid Asset ID"
            else:
                rbx_asset_error = f"{data.status_code}: Error getting Catalog Asset Data"
            glob_vars.rbx_asset_error = rbx_asset_error   
    return rbx_asset_name, rbx_asset_type_id, rbx_asset_creator, rbx_asset_error


### Get Accessory Type name from disctionary of types
def check_asset_type(rbx_asset_type_id, rbx_is_bundle):
    rbx_asset_types = glob_vars.rbx_asset_types
    rbx_bundle_types = glob_vars.rbx_bundle_types
    rbx_asset_error = None
    glob_vars.rbx_asset_error = None
    if rbx_is_bundle:
        rbx_asset_type = rbx_bundle_types.get(rbx_asset_type_id)
        if rbx_asset_type == None:
            rbx_asset_error = "Unknown Bundle Type"
            glob_vars.rbx_asset_error = rbx_asset_error
    else:
        rbx_asset_type = rbx_asset_types.get(rbx_asset_type_id)
        if rbx_asset_type == None:
            rbx_asset_error = "Unknown Asset Type"
            glob_vars.rbx_asset_error = rbx_asset_error
    glob_vars.rbx_asset_type = rbx_asset_type
    return rbx_asset_type, rbx_asset_error
        

### Check if the accessory is supported by Toolbox
def check_supported_type(rbx_asset_type_id, rbx_is_bundle):
    rbx_supported_asset_types = glob_vars.supported_assets
    rbx_supported_bundle_types = glob_vars.supported_bundles

    if rbx_is_bundle:
        rbx_supported_dict = rbx_supported_bundle_types
    else:
        rbx_supported_dict = rbx_supported_asset_types

    for key, value in rbx_supported_dict.items():
        if rbx_asset_type_id in value:
            rbx_supported_type_category = key
            rbx_supported_type = True
            glob_vars.rbx_supported_type = rbx_supported_type
            break
        else:
            rbx_supported_type_category = None
            rbx_supported_type = False
            glob_vars.rbx_supported_type = rbx_supported_type
    return rbx_supported_type, rbx_supported_type_category








##########################################
##### Aceessories specific functions #####
##########################################

### Get Accessory Preview Image URL
def get_asset_and_bundle_img_url(rbx_asset_id, rbx_is_bundle):
    rbx_size = '250x250'
    rbx_format = 'Png'
    rbx_isCircular = 'false'
    if rbx_is_bundle:
        url = f"https://thumbnails.roblox.com/v1/bundles/thumbnails?bundleIds={rbx_asset_id}&size=150x150&format={rbx_format}&isCircular={rbx_isCircular}"
    else:
        url = f"https://thumbnails.roblox.com/v1/assets?assetIds={rbx_asset_id}&returnPolicy=PlaceHolder&size={rbx_size}&format={rbx_format}&isCircular={rbx_isCircular}" 
    data, rbx_asset_error = check_thumbnail_api_state(url, "Accessory")
    if rbx_asset_error == None:
        rbx_asset_img_url = data.get("imageUrl") or data.get("data", [{}])[0].get("imageUrl")
    return rbx_asset_img_url, rbx_asset_error


### Get Accessory Preview Image
def get_asset_and_bundle_img(rbx_asset_img_url):
    rbx_asset_error = None
    glob_vars.rbx_asset_error = None 
    image_data = requests.get(rbx_asset_img_url)
    if image_data.status_code == 200:
        image_data = image_data.content
    else:
        rbx_asset_error = f"{image_data.status_code}: Error getting Accessory IMG"
        glob_vars.rbx_asset_error = rbx_asset_error   
    return image_data, rbx_asset_error
    

### Get Data from Assetdelivery API
def get_asset_data(rbx_asset_id, headers):
    asset_data = None
    rbx_asset_error = None
    glob_vars.rbx_asset_error = None
    url = f"https://apis.roblox.com/asset-delivery-api/v1/assetId/{rbx_asset_id}"
    try:
        response = requests.get(url, headers=headers)
    except:     
        rbx_asset_error = "Error Connecting to Assetdelivery API"
        glob_vars.rbx_asset_error = rbx_asset_error
    else:
        if response.status_code == 200:
            json_data = json.loads(response.content)
            dprint("Asset json_data: " , json_data)
            asset_url = json_data.get("location")
            if asset_url:
                try:
                    asset_response = requests.get(asset_url)
                except:     
                    rbx_asset_error = "Error Connecting to Auth Asset Data URL"
                    glob_vars.rbx_asset_error = rbx_asset_error
                else:
                    if asset_response.status_code == 200:
                        asset_data = asset_response.content
                    else:
                        rbx_asset_error = f"{response.status_code}: Error getting Asset Data"
                        glob_vars.rbx_asset_error = rbx_asset_error
        else:
            rbx_asset_error = f"{response.status_code}: Error getting Asset Data URL"
            glob_vars.rbx_asset_error = rbx_asset_error   
    return asset_data, rbx_asset_error


### Regex finding
def regex(item:str,data:bytes):
    str = data.decode('utf-8', errors='ignore')
    dprint("Regex loking for: " , item)
    rbx_is_roblox_item = False
    if glob_vars.rbx_asset_creator == "Roblox":
        rbx_is_roblox_item = True
    if not rbx_is_roblox_item:
        exp = glob_vars.regex_values_norm.get(item).lower()
        dprint("Regex using normal expressions")
    else:
        #RBXM
        if str.startswith("<roblox!"): 
            exp = glob_vars.regex_values_rbx.get(item).lower()
            dprint("Regex using rbxm Roblox expressions")
            #RBXMX
        if str.startswith("<roblox xmlns"): 
            exp = glob_vars.regex_values_rbxmx.get(item).lower()
            dprint("Regex using rbxmx Roblox expressions")
    clean = r"[0-9]+\W*(prop)"
    str = str.lower()
    res = re.search(exp, str, re.MULTILINE)
    if res == None:
        pass
    else:
        if rbx_is_roblox_item:
            res = res.group()
            if 'id=' in res:
                res = res.split("id=")[1]
            if 'id://' in res:
                res = res.split("id://")[1]
            res = res.split("<")[0]
            if res.endswith("prop"):
                res = res.split("prop")[0]
        else:
            res = res.group()
            res = re.search(clean, res, re.MULTILINE)
            if res == None:
                pass
            else:
                res = res.group()
                res = res.split("prop")[0]
    return res


### Get Accessories Hashes Links
def get_asset_hashes(asset_id): 
    rbx_asset_hsh_urls = None
    rbx_asset_error = None
    glob_vars.rbx_asset_error = None
    url = f"https://thumbnails.roblox.com/v1/assets-thumbnail-3d?assetId={asset_id}"
    data, rbx_asset_error = check_thumbnail_api_state(url, "Accessory")                  
    if rbx_asset_error == None:
        rbx_asset_hsh_urls = data.get("imageUrl") or data.get("data", [{}])[0].get("imageUrl") #Get Link to OBJ and Textures Hashes
        rbx_asset_hsh_urls = requests.get(rbx_asset_hsh_urls)
        if rbx_asset_hsh_urls.status_code == 200:
            rbx_asset_hsh_urls = rbx_asset_hsh_urls.json() #Get OBJ and Textures Hashes links
        else:
            rbx_asset_error = f"{rbx_asset_hsh_urls.status_code}: Error getting Accessory hashes"
            glob_vars.rbx_asset_error = rbx_asset_error 
    return rbx_asset_hsh_urls, rbx_asset_error


### Accessories to download and save all files found in rbxm
def download_and_save_all_files_from_id(items_dict:dict, rbx_asset_own_path, headers):
    for item,item_id in items_dict.items():

        ### Handle Gears ###
        if glob_vars.rbx_supported_type_category == "Gear":
            #use original item ID and download tex and obj via 3d thumb, obj there have UV and correct texture only there
            rbx_asset_hsh_urls, rbx_asset_error = get_asset_hashes(glob_vars.rbx_asset_id)
            if not rbx_asset_error:
                if 'Obj' in item:
                    asset_hsh = rbx_asset_hsh_urls['obj']
                else:
                    asset_hsh = rbx_asset_hsh_urls['textures'][0]
                ### Get direct URL from hash ###
                asset_url = get_cdn_url(asset_hsh)
                ### Download file ###
                asset_data, rbx_asset_error = download(asset_url,item,"Accessory")
            else:
                break

        ### Handle all OBJ separately (elif - gear OBJ will not go here)
        elif 'Obj' in item:
            #use original item ID instead of mesh ID found, because mesh asset dont have UVs
            rbx_asset_hsh_urls, rbx_asset_error = get_asset_hashes(glob_vars.rbx_asset_id)
            if not rbx_asset_error: 
                asset_hsh = rbx_asset_hsh_urls['obj']
                asset_url = get_cdn_url(asset_hsh)
                asset_data, rbx_asset_error = download(asset_url,item,"Accessory")
            else:
                break

        ### Handle all Cages separately (it is also OBJ and also using 3 thumb API to get OBJ file)
        elif 'cage' in item:
            #use original item ID instead of mesh ID found, because mesh asset dont have UVs
            rbx_asset_hsh_urls, rbx_asset_error = get_asset_hashes(item_id)
            if not rbx_asset_error: 
                asset_hsh = rbx_asset_hsh_urls['obj']
                asset_url = get_cdn_url(asset_hsh)
                asset_data, rbx_asset_error = download(asset_url,item,"Accessory")
            else:
                break
        
        ### all other items download via assetdelivery API
        else:
            asset_data, rbx_asset_error = get_asset_data(item_id, headers)


        ### Save downloaded files ###
        if not rbx_asset_error:
            if 'Obj' in item:
                tmp_file_path = os.path.join(rbx_asset_own_path, glob_vars.rbx_asset_name_clean + ".obj")
            elif 'cage' in item:
                tmp_file_path = os.path.join(rbx_asset_own_path, glob_vars.rbx_asset_name_clean + f"_{item}.obj")
            else:
                tmp_file_path = os.path.join(rbx_asset_own_path, glob_vars.rbx_asset_name_clean + f"_{item}.png")

            ### Save file ###
            if not rbx_asset_error:
                save_to_file(tmp_file_path,asset_data,item,"Accessory")
            else:
                break

        








######################################
##### Bundles Specific functions #####
######################################

### Get Catalog information for Bundles
def get_catalog_bundle_data(rbx_asset_id, headers, rbx_char):
    rbx_bundledItems = None
    rbx_asset_name = None
    rbx_asset_type_id = None
    rbx_asset_creator = None
    rbx_asset_error = None
    glob_vars.rbx_asset_error = None
    url = f"https://catalog.roblox.com/v1/catalog/items/{rbx_asset_id}/details?itemType=Bundle"
    try:
        data = requests.get(url, headers=headers)
    except:     
        rbx_asset_error = "Error Getting Catalog Bundle Data"
        glob_vars.rbx_asset_error = rbx_asset_error
    else:
        if data.status_code == 200:
            data = data.json()
            rbx_bundledItems = data["bundledItems"] # will get list of dictionaries with items
            rbx_asset_name = data["name"]
            rbx_asset_type_id = data["bundleType"] 
            rbx_asset_creator = data["creatorName"]
            if rbx_char == 'preview_accessory':
                glob_vars.rbx_asset_name = rbx_asset_name
                glob_vars.rbx_asset_creator = rbx_asset_creator
        else:
            if data.status_code == 404:
                rbx_asset_error = f"{data.status_code}: Invalid Bundle ID"
            else:
                rbx_asset_error = f"{data.status_code}: Error getting Catalog Bundle Data"
            glob_vars.rbx_asset_error = rbx_asset_error   
    return rbx_asset_name, rbx_asset_type_id, rbx_asset_creator, rbx_bundledItems, rbx_asset_error


### Get Accessories Hashes Links
def get_outfit_hashes(outfit_id): 
    rbx_outfit_hsh_urls = None
    rbx_asset_error = None
    glob_vars.rbx_asset_error = None
    url = f"https://thumbnails.roblox.com/v1/users/outfit-3d?outfitId={outfit_id}"
    data, rbx_asset_error = check_thumbnail_api_state(url, "Accessory")                  
    if rbx_asset_error == None:
        rbx_outfit_hsh_urls = data.get("imageUrl") or data.get("data", [{}])[0].get("imageUrl") #Get Link to OBJ and Textures Hashes
        rbx_outfit_hsh_urls = requests.get(rbx_outfit_hsh_urls)
        if rbx_outfit_hsh_urls.status_code == 200:
            rbx_outfit_hsh_urls = rbx_outfit_hsh_urls.json() #Get OBJ and Textures Hashes links
        else:
            rbx_asset_error = f"{rbx_outfit_hsh_urls.status_code}: Error getting Outfit hashes"
            glob_vars.rbx_asset_error = rbx_asset_error 
    return rbx_outfit_hsh_urls, rbx_asset_error


### Check which bundle the bundled item is belon to
def find_bundle_id_from_bundled_item(bundled_item_id):
    rbx_bundle_id = None
    rbx_asset_error = None
    rbx_bundle_name = None
    glob_vars.rbx_asset_error = None
    url = f"https://catalog.roblox.com/v1/assets/{bundled_item_id}/bundles?limit=10&sortOrder=Asc"  
    try:
        response = requests.get(url)
    except:     
        rbx_asset_error = "Error Connecting to Catalog API"
        glob_vars.rbx_asset_error = rbx_asset_error
    else:
        if response.status_code == 200:
            data = response.json()
            data = data.get("data")[0]
            rbx_bundle_id = data.get("id")
            rbx_bundle_name = data.get("name")
        if response.status_code == 400:
            rbx_asset_error = f"{response.status_code}: Invalid Asset ID"
        else:
            rbx_asset_error = f"{response.status_code}: Error getting Catalog Asset Data"
        glob_vars.rbx_asset_error = rbx_asset_error 
    return rbx_bundle_id, rbx_bundle_name, rbx_asset_error


def filter_bundled_items(rbx_bundledItems):
    rbx_outfits = ["UserOutfit"]
    rbx_skippable_names = ["Default Mood"]
    rbx_bundledItems_name_and_id_filtered_dict = {} # item_name : item_id
    rbx_bundledItemsoutfits_name_and_id_filtered_list = [] # item_name : item_id

    for rbx_bundled_item in rbx_bundledItems:
        rbx_temp_outfit_dict = {} # item_name : item_id
        rbx_bundled_item_id = rbx_bundled_item["id"]
        rbx_bundled_item_name = rbx_bundled_item["name"]
        rbx_bundled_item_type = rbx_bundled_item["type"]
        if rbx_bundled_item_type in rbx_outfits:
            rbx_temp_outfit_dict[rbx_bundled_item_name] = rbx_bundled_item_id
            rbx_bundledItemsoutfits_name_and_id_filtered_list.append(rbx_temp_outfit_dict)
        if rbx_bundled_item_type != "Asset":
            continue
        if rbx_bundled_item_name in rbx_skippable_names:
            continue
        rbx_bundledItems_name_and_id_filtered_dict[rbx_bundled_item_name] = rbx_bundled_item_id
    return rbx_bundledItems_name_and_id_filtered_dict, rbx_bundledItemsoutfits_name_and_id_filtered_list


def check_supported_bundled_items(filtered_dict_of_bundled_items:dict, headers, rbx_char):
    rbx_bundledItems_name_and_type_supported_list_of_dict = []
    rbx_supported_bundled_items = glob_vars.supported_bundled_items
    rbx_asset_error = None
    rbx_bundled_asset_type_name = None
    glob_vars.rbx_asset_error = rbx_asset_error

    for item_name, item_id in filtered_dict_of_bundled_items.items():
        rbx_tmp_dict = {}
        rbx_bundled_asset_name, rbx_bundled_asset_type_id, rbx_asset_creator, rbx_asset_error = get_catalog_asset_data(item_id, headers, rbx_char)
        if not rbx_asset_error:
            rbx_bundled_asset_type = rbx_supported_bundled_items.get(rbx_bundled_asset_type_id)
            if rbx_bundled_asset_type == None:
                ### Check if asset attached to the bundle is supported
                rbx_supported_type, rbx_bundled_asset_type = check_supported_type(rbx_bundled_asset_type_id, False)
                if rbx_bundled_asset_type == None:
                    rbx_asset_error = f"Error. Unsupported item found (Asset ID: {rbx_bundled_asset_type_id})"
                    glob_vars.rbx_asset_error = rbx_asset_error
                    break
            ### get bundled item its own asset type name (for textures finding later)
            for type_name, values_list in glob_vars.supported_assets.items():
                if rbx_bundled_asset_type_id in values_list:
                    rbx_bundled_asset_type_name = type_name
                    break

            rbx_tmp_dict["name"] = item_name
            rbx_tmp_dict["id"] = item_id
            rbx_tmp_dict["assetType"] = rbx_bundled_asset_type
            rbx_tmp_dict["assetTypeName"] = rbx_bundled_asset_type_name
            rbx_bundledItems_name_and_type_supported_list_of_dict.append(rbx_tmp_dict)
        else:
            break
    return rbx_bundledItems_name_and_type_supported_list_of_dict,rbx_asset_error




### Accessories to download and save all files found in rbxm (bundles only)
def download_and_save_all_bundle_files_from_id(items_dict:dict, rbx_asset_own_path, rbx_supported_type_category, rbx_bundle_asset_id, rbx_bundled_asset_name_clean, headers):
    ### item_id - its an ID found in RBXM for Tex and OBJ
    ### rbx_bundle_asset_id - actual ID of an item itself
    for item,item_id in items_dict.items():
        
        ### Handle Dynamic Heads (only OBJ, tex will not come here)
        if rbx_supported_type_category == "Dynamic Head" and 'Obj' in item:
            dprint("CHECKED is DYNAMIC HEAD")
            #use original item ID instead of mesh ID found, because mesh asset dont have UVs
            asset_data, rbx_asset_error = get_asset_data(item_id, headers)

        ### Handle all OBJ separately (elif - gear OBJ will not go here)
        elif 'Obj' in item:
            #use original item ID instead of mesh ID found, because mesh asset dont have UVs
            rbx_asset_hsh_urls, rbx_asset_error = get_asset_hashes(rbx_bundle_asset_id)
            if not rbx_asset_error: 
                asset_hsh = rbx_asset_hsh_urls['obj']
                asset_url = get_cdn_url(asset_hsh)
                asset_data, rbx_asset_error = download(asset_url,item,"Accessory")
            else:
                break

        ### Handle all Cages separately (it is also OBJ and also using 3 thumb API to get OBJ file)
        elif 'cage' in item:
            #use original item ID instead of mesh ID found, because mesh asset dont have UVs
            rbx_asset_hsh_urls, rbx_asset_error = get_asset_hashes(item_id)
            if not rbx_asset_error: 
                asset_hsh = rbx_asset_hsh_urls['obj']
                asset_url = get_cdn_url(asset_hsh)
                asset_data, rbx_asset_error = download(asset_url,item,"Accessory")
            else:
                break
        
        ### all other items download via assetdelivery API
        else:
            asset_data, rbx_asset_error = get_asset_data(item_id, headers)

        ### Save downloaded files ###
        if not rbx_asset_error:
            if 'Obj' in item:
                tmp_file_path = os.path.join(rbx_asset_own_path, rbx_bundled_asset_name_clean + ".obj")
            elif 'cage' in item:
                tmp_file_path = os.path.join(rbx_asset_own_path, rbx_bundled_asset_name_clean + f"_{item}.obj")
            else:
                tmp_file_path = os.path.join(rbx_asset_own_path, rbx_bundled_asset_name_clean + f"_{item}.png")

            ### Save file ###
            if not rbx_asset_error:
                save_to_file(tmp_file_path,asset_data,item,"Accessory")
            else:
                break


### Write extensions into MTL (roblox mtl dont show .png, so blender images not displaying)
def write_png_ext_into_mtl(mtl_file, tex_hsh:list):
    error = None
    glob_vars.rbx_asset_error = None
    try:
        with open(mtl_file, 'r', encoding='UTF-8') as f:
            text = f.read()
    except:
        error = "Error writing to MTL file"
        glob_vars.rbx_asset_error = error
    else:
        with open(mtl_file, 'w', encoding='UTF-8') as f:
            for i in range(len(tex_hsh)):
                text = text.replace(tex_hsh[i], tex_hsh[i] + ".png")
            f.write(text)
    return error
    






#################################
##### Blender API functions #####
#################################

def blender_api_import_obj(obj_filepath):
    if glob_vars.bldr_ver[0] < '4':
        bpy.ops.import_scene.obj(filepath=obj_filepath)
    else:
        bpy.ops.wm.obj_import(filepath=obj_filepath)
    return


def blender_api_assets_new_material(rbx_asset_own_path, rbx_asset_items_dict:dict, asset_name_clean):
    ### Creating new Material ###
    rbx_obj = bpy.context.selected_objects[0]
    bpy.ops.object.select_all(action='DESELECT')
    bpy.context.view_layer.objects.active = None
    bpy.data.objects[rbx_obj.name].select_set(True)
    bpy.context.view_layer.objects.active = bpy.data.objects[rbx_obj.name]
    
    if rbx_obj.material_slots:
        bpy.ops.object.material_slot_remove()
    mat = bpy.data.materials.new(name=f"{asset_name_clean}_mat")
    rbx_obj.data.materials.append(mat) 
    mat = rbx_obj.material_slots[0].material 
    mat.use_nodes = True
    mat.use_backface_culling = True
    nodes = mat.node_tree.nodes
    bsdf = nodes.get("Principled BSDF")
    if float(glob_vars.bldr_fdr) < 4.0:
        bsdf.inputs[9].default_value = 1
    else:
        bsdf.inputs[2].default_value = 1
    
    node_y_index = 0
    for rbx_tex_name in rbx_asset_items_dict.keys():
        if rbx_tex_name == "Obj" or "cage" in rbx_tex_name:
            continue    # Skip Obj and Cages
        rbx_tex = os.path.join(rbx_asset_own_path, asset_name_clean + f"_{rbx_tex_name}.png")
        rbx_image = bpy.data.images.load(rbx_tex)
        rbxtexNode = nodes.new('ShaderNodeTexImage')
        rbxtexNode.image = rbx_image
        rbxtexNode.name = rbx_tex_name
        rbxtexNode.location = (-500,300-300 * node_y_index)
        if rbx_tex_name == "texture" or rbx_tex_name == "base_color":
            mat.node_tree.links.new(rbxtexNode.outputs[0], bsdf.inputs["Base Color"])
        elif rbx_tex_name == "Normal":
            norm_node = nodes.new(type="ShaderNodeNormalMap")
            norm_node.location = (-200,300-300 * node_y_index)        
            mat.node_tree.links.new(rbxtexNode.outputs[0], norm_node.inputs[1])
            mat.node_tree.links.new(norm_node.outputs[0], bsdf.inputs[rbx_tex_name])
            norm_node.space = 'TANGENT'
            rbx_image.colorspace_settings.name = 'Non-Color'
        else:
            mat.node_tree.links.new(rbxtexNode.outputs[0], bsdf.inputs[rbx_tex_name])
            rbx_image.colorspace_settings.name = 'Non-Color'
        node_y_index += 1


def blender_api_assets_reposition(move_x_axis: float = False):
    ### Position Asset ###
    bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY', center='MEDIAN')
    bpy.ops.view3d.snap_selected_to_cursor(use_offset=False)
    bpy.ops.transform.rotate(value=3.14159, orient_axis='Z', orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL')
    if move_x_axis:
        bpy.ops.transform.translate(value=(move_x_axis, 0, 0), orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', constraint_axis=(True, False, False))

    
def blender_api_assets_remove_doubles():
    ### Removing doubles ###
    if bpy.context.mode == 'OBJECT':
        bpy.ops.object.editmode_toggle()
        bpy.ops.mesh.select_all(action='SELECT')                
    elif bpy.context.mode == 'EDIT_MESH':
        bpy.ops.mesh.select_all(action='SELECT')
    bpy.ops.mesh.remove_doubles()
    bpy.ops.object.editmode_toggle()
    bpy.ops.mesh.customdata_custom_splitnormals_clear()
    if float(glob_vars.bldr_fdr) < 4.1:
        bpy.context.object.data.use_auto_smooth = False
    else:
        bpy.ops.object.shade_flat()
    bpy.ops.object.shade_smooth()



'''if float(glob_vars.bldr_fdr) < 3.4:
    rbx_MixNode = rbx_nodes.new('ShaderNodeMixRGB')
    rbx_MixNode.inputs[1].default_value = (rbx_shade_r, rbx_shade_g, rbx_shade_b, 1)
    else:
    rbx_MixNode = rbx_nodes.new('ShaderNodeMix')
    rbx_MixNode.data_type='RGBA'
    rbx_MixNode.inputs[6].default_value = (rbx_shade_r, rbx_shade_g, rbx_shade_b, 1)
    rbx_MixNode.location = (-200,300)

    rbx_img = rbx_nodes['Image Texture']
    rbx_img.location = (-500,300)
    rbx_img_link = rbx_img.outputs[0].links[0] #existing link to bsdf
    rbx_mat.node_tree.links.remove(rbx_img_link) #remove existing link to bsdf

    if float(glob_vars.bldr_fdr) < 3.4:
    rbx_mat.node_tree.links.new(rbx_img.outputs[1], rbx_MixNode.inputs[0]) #Alpha
    rbx_mat.node_tree.links.new(rbx_img.outputs[0], rbx_MixNode.inputs[2]) #Color
    rbx_mat.node_tree.links.new(rbx_MixNode.outputs[0], bsdf.inputs[0])
    else:
    rbx_mat.node_tree.links.new(rbx_img.outputs[1], rbx_MixNode.inputs[0]) #Alpha
    rbx_mat.node_tree.links.new(rbx_img.outputs[0], rbx_MixNode.inputs[7]) #Color
    rbx_mat.node_tree.links.new(rbx_MixNode.outputs[2], bsdf.inputs[0])'''


### remove alpha textures and add a mix node to properly display transparency
def blender_api_transparent_textures():
    if float(glob_vars.bldr_fdr) < 3.4:
        obj = bpy.context.selected_objects[0]
        bpy.ops.object.select_all(action='DESELECT')
        bpy.context.view_layer.objects.active = None
        bpy.data.objects[obj.name].select_set(True)
        bpy.context.view_layer.objects.active = bpy.data.objects[obj.name]
    else:
        obj = bpy.context.active_object

    if obj is None or obj.type != 'MESH':
        print("Please select a mesh object.")
    else:
        for slot in obj.material_slots:
            mat = slot.material
            if mat is None or not mat.use_nodes:
                print(f"Skipping empty or non-node material in slot: {slot.name}")
                continue
            
            # Setup backface culling
            mat.show_transparent_back = False
            mat.use_backface_culling = True 

            nodes = mat.node_tree.nodes
            links = mat.node_tree.links

            # Find the Principled BSDF node
            bsdf_node = None
            for node in nodes:
                if node.type == 'BSDF_PRINCIPLED':
                    bsdf_node = node
                    break

            if bsdf_node is None:
                print(f"No Principled BSDF found in material: {mat.name}")
                continue

            base_color_input = bsdf_node.inputs[0]
            alpha_input = bsdf_node.inputs[4]

            # Get base color image texture
            base_color_link = base_color_input.links[0] if base_color_input.is_linked else None
            base_color_tex = base_color_link.from_node if base_color_link else None

            # Remove transparency node connected to alpha input (if exists)
            if alpha_input.is_linked:
                alpha_link = alpha_input.links[0]
                alpha_node = alpha_link.from_node
                links.remove(alpha_link)
                nodes.remove(alpha_node)
                print(f"Removed transparency texture node in material: {mat.name}")
            else:
                print(f"No alpha texture to remove in material: {mat.name}")

            if not base_color_tex or base_color_tex.type != 'TEX_IMAGE':
                print(f"Material {mat.name}: Base color is not connected to an image texture.")
                continue

            # Remove link from base color texture to BSDF base color
            links.remove(base_color_link)

            # Create MixRGB node
            mix_node = nodes.new(type='ShaderNodeMixRGB')
            mix_node.blend_type = 'MIX'
            mix_node.label = 'Alpha Mix'
            rbx_shade_r = 0.361304
            rbx_shade_g = 0.3564
            rbx_shade_b = 0.371238
            mix_node.inputs[1].default_value = (rbx_shade_r, rbx_shade_g, rbx_shade_b, 1)  # fallback color
            #mix_node.location = ((base_color_tex.location.x + bsdf_node.location.x) / 8 * 5, base_color_tex.location.y - 0)
            mix_node.location = (bsdf_node.location.x - 200, base_color_tex.location.y - 0)

            # Connect image color → Mix input 2
            links.new(base_color_tex.outputs['Color'], mix_node.inputs[2])

            # Connect image alpha → Mix Fac
            if 'Alpha' in base_color_tex.outputs:
                links.new(base_color_tex.outputs['Alpha'], mix_node.inputs[0])
            else:
                print(f"Material {mat.name}: Texture has no Alpha output.")

            # Connect Mix → BSDF base color
            links.new(mix_node.outputs['Color'], bsdf_node.inputs[0])










class OBJECT_OT_add_object(bpy.types.Operator,AddObjectHelper): # type: ignore
    """Create a new Mesh Object"""
    bl_idname = "object.add_character"
    bl_label = "Add Roblox Character"
    bl_options = {'REGISTER', 'UNDO'}
    rbx_char : bpy.props.StringProperty(name= "Added") # type: ignore


    def execute(self, context): 
        scene = context.scene
        rbx_char = self.rbx_char
        rbx_prefs = scene.rbx_prefs
        rbx_username_entered = rbx_prefs.rbx_username_entered
        rbx_split = rbx_prefs.rbx_split 
        rbx_accessory_entered = rbx_prefs.rbx_accessory_entered
        rbx_incl_cages = rbx_prefs.rbx_incl_cages 

        
        # Run async function from sync context and refresh Auth Token if need
        try:
            loop = asyncio.get_event_loop()
        except RuntimeError:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)

        access_token = loop.run_until_complete(renew_token(context))
        headers = {
            "Authorization": f"Bearer {access_token}"
        }

        ### Create import characters folder
        create_folders(rbx_char, addon_path)







        ##### Character Preview #####
        if rbx_char == 'preview_avatar':
            ### Set username and user ID
            rbx_username_or_id, username_field_is, rbx_char_error = check_username_field_and_extract_id(rbx_username_entered)
            if rbx_char_error == None:
                if username_field_is != 'id':
                    rbx_user_name = rbx_username_or_id
                    rbx_user_id, rbx_char_error = get_user_id(rbx_user_name, headers)
                else:
                    rbx_user_id = rbx_username_or_id
                    rbx_user_name, rbx_char_error = get_user_name(rbx_user_id, headers)
                rbx_user_name_clean = replace_restricted_char(rbx_user_name)
                glob_vars.rbx_user_name_clean = rbx_user_name_clean
                

            ### Get Profile Avatar URL
            if rbx_char_error == None:
                rbx_usr_img_url, rbx_char_error = get_user_avatar_url(rbx_user_id)
            
            ### Get Profile Avatar IMG
            if rbx_char_error == None:
                rbx_usr_avtr, rbx_char_error = get_user_avatar_img(rbx_usr_img_url)
            
            ### Clear Previous Preview ###
            if rbx_char_error == None:
                try:
                    rbx_tmp_img = bpy.data.images[rbx_user_name_clean + '.png']
                    bpy.data.images.remove(rbx_tmp_img)
                except:
                    pass

            if rbx_char_error == None:     
                rbx_tmp_filepath = os.path.join(glob_vars.addon_path, glob_vars.rbx_import_main_folder, 'tmp')
                if not os.path.exists(rbx_tmp_filepath):
                    os.makedirs(rbx_tmp_filepath)
                rbx_tmp_file = os.path.join(rbx_tmp_filepath, rbx_user_name_clean + ".png")
                
                try:
                    with open(f"{rbx_tmp_file}", "wb") as f:
                        f.write(rbx_usr_avtr) 
                except:
                    rbx_char_error = "Error saving temp avatar img"
                else:
                    rbx_usr_avtr = bpy.data.images.load(rbx_tmp_file)


        



        ##### Accessory Preview #####
        if rbx_char == 'preview_accessory':
            ### Disable Import button and set all names to none
            glob_vars.rbx_supported_type = False
            glob_vars.rbx_asset_name = None
            glob_vars.rbx_asset_name_clean = None
            glob_vars.rbx_asset_creator = None
            glob_vars.rbx_asset_type = None
            rbx_prefs.rbx_incl_cages = False
            glob_vars.rbx_is_bundled_item = False

            ### Extract Accessory ID
            rbx_asset_id, rbx_is_bundle, rbx_asset_error = check_accessory_field_and_extract_id(rbx_accessory_entered)
            glob_vars.rbx_asset_id = rbx_asset_id
            dprint("rbx_asset_id: " , rbx_asset_id)
            dprint("rbx_is_bundle: " , rbx_is_bundle)

            ### Get asset type ID, name, creator
            if rbx_asset_error == None:
                if not rbx_is_bundle:
                    rbx_asset_name, rbx_asset_type_id, rbx_asset_creator, rbx_asset_error = get_catalog_asset_data(rbx_asset_id, headers, rbx_char)
                    if rbx_asset_error: #if digits entered as asset ID try also check if its bundle
                        rbx_asset_name, rbx_asset_type_id, rbx_asset_creator,rbx_bundledItems, rbx_asset_error = get_catalog_bundle_data(rbx_asset_id, headers, rbx_char)
                        if not rbx_asset_error:
                            rbx_is_bundle = True
                            glob_vars.rbx_is_bundle = rbx_is_bundle
                else:
                    rbx_asset_name, rbx_asset_type_id, rbx_asset_creator,rbx_bundledItems, rbx_asset_error = get_catalog_bundle_data(rbx_asset_id, headers, rbx_char)
                dprint("rbx_asset_name: " , rbx_asset_name)
                dprint("rbx_asset_type_id: " , rbx_asset_type_id)
                dprint("rbx_is_bundled_item: " , glob_vars.rbx_is_bundled_item)

            
            ### Get Item Type
            if rbx_asset_error == None:
                rbx_asset_type, rbx_asset_error = check_asset_type(rbx_asset_type_id, rbx_is_bundle)
                dprint("rbx_asset_type: " , rbx_asset_type)


            ### Clean Accessory Name
            if rbx_asset_error == None:
                rbx_asset_name_clean = replace_restricted_char(rbx_asset_name)
                glob_vars.rbx_asset_name_clean = rbx_asset_name_clean
            
            ### Get Preview Image URL
            if rbx_asset_error == None:
                rbx_asset_img_url, rbx_asset_error = get_asset_and_bundle_img_url(rbx_asset_id, rbx_is_bundle)

            ### Get Accessory IMG
            if rbx_asset_error == None:
                rbx_asset_thumb_img, rbx_asset_error = get_asset_and_bundle_img(rbx_asset_img_url)

            ### Clear Previous Preview ###
            if rbx_asset_error == None:
                try:
                    rbx_tmp_img = bpy.data.images[rbx_asset_name_clean + '.png']
                    bpy.data.images.remove(rbx_tmp_img)
                except:
                    pass
            
            ### Save preview file thumb
            if rbx_asset_error == None:     
                rbx_tmp_filepath = os.path.join(glob_vars.addon_path, glob_vars.rbx_import_main_folder, 'tmp')
                if not os.path.exists(rbx_tmp_filepath):
                    os.makedirs(rbx_tmp_filepath)
                rbx_tmp_file = os.path.join(rbx_tmp_filepath, rbx_asset_name_clean + ".png")
                
                try:
                    with open(f"{rbx_tmp_file}", "wb") as f:
                        f.write(rbx_asset_thumb_img) 
                except:
                    rbx_asset_error = "Error saving temp avatar img"
                    glob_vars.rbx_asset_error = rbx_asset_error
                else:
                    rbx_asset_thumb_img = bpy.data.images.load(rbx_tmp_file)

            ### Check if supported Item
            if rbx_asset_error == None:
                rbx_supported_type, rbx_supported_type_category = check_supported_type(rbx_asset_type_id, rbx_is_bundle)
                glob_vars.rbx_supported_type_category = rbx_supported_type_category
                dprint("rbx_supported_type: " , rbx_supported_type)
                dprint("rbx_supported_type_category: " , rbx_supported_type_category)
            
            if not rbx_asset_error: #check if asset is actually part of bundle
                if rbx_asset_type_id in glob_vars.part_of_bundle_items:
                    rbx_is_bundle = True
                    glob_vars.rbx_is_bundle = rbx_is_bundle
                    glob_vars.rbx_is_bundled_item = True


            
            




        ##### Accessory Import #####
        ### This button should be disabled if accessory is not supported
        if rbx_char == 'import_accessory':

            ### if item is part of bundle, find bundle ID and bundle name
            if glob_vars.rbx_is_bundled_item:
                ### find original bundle ID
                rbx_bundle_id, rbx_bundle_name, rbx_asset_error = find_bundle_id_from_bundled_item(glob_vars.rbx_asset_id)
                glob_vars.rbx_asset_id = rbx_bundle_id

                ### Clean Accessory Name
                if not rbx_asset_error:
                    rbx_asset_name_clean = replace_restricted_char(rbx_bundle_name)
                    glob_vars.rbx_asset_name_clean = rbx_asset_name_clean

            
            ###########################################
            # ### Handle all bundles
            if glob_vars.rbx_is_bundle:
                rbx_asset_name, rbx_asset_type_id, rbx_asset_creator,rbx_bundledItems, rbx_asset_error = get_catalog_bundle_data(glob_vars.rbx_asset_id, headers, rbx_char)
                dprint("rbx_bundledItems: " , rbx_bundledItems)

                ### Filter out not necessary items and get only asset name and ID
                ### Then check supported assets inside and get their type names
                if not rbx_asset_error:
                    rbx_bundledItems_name_and_id_filtered_dict, rbx_bundledItemsoutfits_name_and_id_filtered_list = filter_bundled_items(rbx_bundledItems)
                    dprint("rbx_bundledItemsoutfits_name_and_id_filtered_list: ", rbx_bundledItemsoutfits_name_and_id_filtered_list)

                    rbx_bundledItems_name_and_type_supported_list_of_dict,rbx_asset_error = check_supported_bundled_items(rbx_bundledItems_name_and_id_filtered_dict, headers, rbx_char)
                    dprint("rbx_bundledItems_name_and_type_supported_list_of_dict: ", rbx_bundledItems_name_and_type_supported_list_of_dict)

                ### Create Accessory own folder
                if rbx_asset_error == None:
                    rbx_asset_own_path = os.path.join(glob_vars.addon_path, glob_vars.rbx_import_main_folder, glob_vars.rbx_imported_acc_fldr, glob_vars.rbx_asset_name_clean)
                    if not os.path.exists(rbx_asset_own_path):
                        os.makedirs(rbx_asset_own_path)



                ###########################################
                #### Handle Shoes only
                if glob_vars.rbx_supported_type_category == "Shoes":

                    #### loop through all items in the bundle:
                    #rbx_bundled_asset_items_list_of_dict = []
                    rbx_bundle_loop_counter = 0
                    for rbx_bundled_item_dict in rbx_bundledItems_name_and_type_supported_list_of_dict:
                        ### Define list to iterate throug items every loop
                        rbx_asset_sets_rbxm_lst = []
                        dprint("rbx_bundled_item_dict: ", rbx_bundled_item_dict)

                        ### Set bundled item its own asset category name (replace the category name taken during preview asset)
                        rbx_supported_type_category = rbx_bundled_item_dict.get("assetTypeName")

                        ### Get item ID from the list
                        rbx_bundled_item_id = rbx_bundled_item_dict.get("id")

                        ### Get clean name for the bundled accessory
                        rbx_bundled_item_name = rbx_bundled_item_dict.get("name")
                        rbx_bundled_asset_name_clean = replace_restricted_char(rbx_bundled_item_name)

                        ### Get rbxm to Find obj id and all textures id
                        if not rbx_asset_error:
                            asset_data, rbx_asset_error = get_asset_data(rbx_bundled_item_id, headers)

                        ### Find all accessory values in rbxm
                        if rbx_asset_error == None:
                            rbx_asset_items_dict = {} # where rbxm ID's supposed to be saved
                            rbx_asset_sets_rbxm_lst = glob_vars.rbx_asset_sets_rbxm.get(rbx_supported_type_category)    #get required sets to be look in rbxm (list)
                            if rbx_incl_cages and rbx_supported_type_category == "Layered Cloth":
                                cages_list = glob_vars.rbx_asset_sets_rbxm.get("Cages")
                                for cage in cages_list:
                                    rbx_asset_sets_rbxm_lst.append(cage)
                            
                            dprint("rbx_asset_sets_rbxm_lst: ", rbx_asset_sets_rbxm_lst)
                            for item in rbx_asset_sets_rbxm_lst:
                                asset_item_id = regex(item, asset_data)
                                if not asset_item_id and item == "base_color":
                                    asset_item_id = regex("texture", asset_data)    # LC without PBR maps no base color, is texture
                                if not asset_item_id:
                                    rbx_raise_error_items = glob_vars.rbxm_raise_error_if_not_found.get(rbx_supported_type_category)
                                    if rbx_incl_cages:
                                        cages_list = glob_vars.rbxm_raise_error_if_not_found.get("Cages")
                                        for cage in cages_list:
                                            rbx_raise_error_items.append(cage)
                                    if item in rbx_raise_error_items:
                                        rbx_asset_error = f"Error: Failed to find {item} ID in RBXM"
                                        glob_vars.rbx_asset_error = rbx_asset_error
                                        break
                                    else:
                                        continue      
                                rbx_asset_items_dict[item] = asset_item_id 
                                dprint(f"{item} ID found in RBXM: ", asset_item_id)  

                            ### Adding all items IDs into the main list
                            #rbx_bundled_asset_items_list_of_dict.append(rbx_asset_items_dict)
                                
                    #print("rbx_bundled_asset_items_list_of_dict: ", rbx_bundled_asset_items_list_of_dict)    

                        ### Download and save all files
                        if rbx_asset_error == None:
                            download_and_save_all_bundle_files_from_id(rbx_asset_items_dict, rbx_asset_own_path, rbx_supported_type_category, rbx_bundled_item_id, rbx_bundled_asset_name_clean, headers)   

                        ### Import Accessory ###    
                        if rbx_asset_error == None:
                            ### Start Accessory Import ###
                            obj_filepath = os.path.join(rbx_asset_own_path, rbx_bundled_asset_name_clean + ".obj")
                            blender_api_import_obj(obj_filepath)
                            blender_api_assets_new_material(rbx_asset_own_path, rbx_asset_items_dict, rbx_bundled_asset_name_clean)
                            if "Left Shoe" in rbx_bundled_item_name or "Right Shoe" in rbx_bundled_item_name:
                                if "Right Shoe" in rbx_bundled_item_name:
                                    move_x_axis_float = -0.3
                                else:
                                    move_x_axis_float = 0.3
                            else:
                                if rbx_bundle_loop_counter == 0:
                                    move_x_axis_float = -0.3
                                else:
                                    move_x_axis_float = 0.3
                            blender_api_assets_reposition(move_x_axis=move_x_axis_float)
                            blender_api_assets_remove_doubles()

                            if rbx_incl_cages:
                                cages_list = glob_vars.rbx_asset_sets_rbxm.get("Cages")
                                for cage in cages_list:
                                    obj_filepath = os.path.join(rbx_asset_own_path, rbx_bundled_asset_name_clean + f"_{cage}.obj")
                                    blender_api_import_obj(obj_filepath)
                                    if rbx_bundle_loop_counter == 0:
                                        move_x_axis_float = 5.0
                                    else:
                                        move_x_axis_float = 8.0
                                    blender_api_assets_reposition(move_x_axis=move_x_axis_float)
                        rbx_bundle_loop_counter +=1
                

                ###########################################
                #### Handle all other bundles
                else:
                    if not rbx_asset_error:
                        ### Get hashes URLs for all outfit IDs in the bundle
                        rbx_outfit_count = 0
                        for outfit_dict in rbx_bundledItemsoutfits_name_and_id_filtered_list:
                            ## take only 1st outfit (for now, to check later)
                            if rbx_outfit_count > 0:
                                continue
                            outfit_name = list(outfit_dict.keys())[0] # this dict should have only 1 record name and id
                            outfit_id = outfit_dict.get(outfit_name)
                            rbx_outfit_hsh_urls, rbx_asset_error = get_outfit_hashes(outfit_id)
                            rbx_outfit_count += 1

                    ### Get hashed URLs of item
                    if not rbx_asset_error: 
                        outfit_obj_hsh = rbx_outfit_hsh_urls['obj']
                        outfit_mtl_hsh = rbx_outfit_hsh_urls['mtl']
                        outfit_tex_hsh = rbx_outfit_hsh_urls['textures']
                        
                        ### Get All URLs ###
                        outfit_mtl_url = get_cdn_url(outfit_mtl_hsh)
                        outfit_obj_url = get_cdn_url(outfit_obj_hsh)

                        ### Add all Tex URL to list ###
                        outfit_tex_url = []
                        if outfit_tex_hsh:
                            for i in range(len(outfit_tex_hsh)):
                                tmp_tex_url = get_cdn_url(outfit_tex_hsh[i])
                                outfit_tex_url.append(tmp_tex_url)

                        dprint("outfit_mtl_url: ", outfit_mtl_url)
                        dprint("outfit_obj_url: ", outfit_obj_url)
                        dprint("outfit_tex_url: ", outfit_tex_url)
                    
                    ### Download files ###
                    if not rbx_asset_error:
                        data, rbx_asset_error = download(outfit_mtl_url,"mtl", "Accessory")
                        ### Save file ###
                        if not rbx_asset_error: 
                            rbx_mtl_file = os.path.join(rbx_asset_own_path, glob_vars.rbx_asset_name_clean + ".mtl")
                            save_to_file(rbx_mtl_file, data, "mtl", "Accessory")
                            if outfit_tex_hsh:
                                rbx_asset_error = write_png_ext_into_mtl(rbx_mtl_file, outfit_tex_hsh)

                    ### Download files ###       
                    if not rbx_asset_error:
                        data, rbx_asset_error = download(outfit_obj_url,"Obj", "Accessory")
                        ### Save file ###
                        if not rbx_asset_error: 
                            rbx_obj_file = os.path.join(rbx_asset_own_path, glob_vars.rbx_asset_name_clean + ".obj")
                            save_to_file(rbx_obj_file, data, "Obj", "Accessory")

                    ### Save textures
                    if not rbx_asset_error:
                        if outfit_tex_url:  #some items no texture at all (not sure how)
                            for i in range(len(outfit_tex_url)):
                                data, rbx_asset_error = download(outfit_tex_url[i],"Texture", "Accessory")
                                if not rbx_asset_error:
                                    rbx_tex_file = os.path.join(rbx_asset_own_path, outfit_tex_hsh[i] + ".png")
                                    save_to_file(rbx_tex_file, data, "Texture", "Accessory")
                                else:
                                    break
                    
                    ### Start Bundle Import ###
                    if not rbx_asset_error:
                        blender_api_import_obj(rbx_obj_file)
                        blender_api_transparent_textures()
                        blender_api_assets_reposition()
                        blender_api_assets_remove_doubles()





            ### Handle all other accessories
            else:
                ### Get rbxm to Find obj id and all textures id
                asset_data, rbx_asset_error = get_asset_data(glob_vars.rbx_asset_id, headers)

                ### Create Accessory own folder
                if rbx_asset_error == None:
                    rbx_asset_own_path = os.path.join(glob_vars.addon_path, glob_vars.rbx_import_main_folder, glob_vars.rbx_imported_acc_fldr, glob_vars.rbx_asset_name_clean)
                    if not os.path.exists(rbx_asset_own_path):
                        os.makedirs(rbx_asset_own_path) 

                ### Find all accessory values in rbxm
                if rbx_asset_error == None:
                    rbx_asset_items_dict = {} # where rbxm ID's supposed to be saved
                    rbx_asset_sets_rbxm_lst = glob_vars.rbx_asset_sets_rbxm.get(glob_vars.rbx_supported_type_category)    #get required sets to be look in rbxm (list)
                    if rbx_incl_cages:
                        cages_list = glob_vars.rbx_asset_sets_rbxm.get("Cages")
                        for cage in cages_list:
                            rbx_asset_sets_rbxm_lst.append(cage)

                    for item in rbx_asset_sets_rbxm_lst:
                        asset_item_id = regex(item, asset_data)
                        if not asset_item_id and item == "base_color":
                            asset_item_id = regex("texture", asset_data)    # LC without PBR maps no base color, is texture
                        if not asset_item_id:
                            rbx_raise_error_items = glob_vars.rbxm_raise_error_if_not_found.get(glob_vars.rbx_supported_type_category)
                            if rbx_incl_cages:
                                cages_list = glob_vars.rbxm_raise_error_if_not_found.get("Cages")
                                for cage in cages_list:
                                    rbx_raise_error_items.append(cage)
                            if item in rbx_raise_error_items:
                                rbx_asset_error = f"Error: Failed to find {item} ID in RBXM"
                                glob_vars.rbx_asset_error = rbx_asset_error
                                break
                            else:
                                continue      
                        rbx_asset_items_dict[item] = asset_item_id
                        dprint(": " , )
                        print(f"{item} ID found in RBXM: ", asset_item_id)

                    ### Download and save all files
                    if rbx_asset_error == None:
                        download_and_save_all_files_from_id(rbx_asset_items_dict, rbx_asset_own_path, headers)

                    ### Import Accessory ###    
                    if rbx_asset_error == None:
                        ### Start Accessory Import ###
                        obj_filepath = os.path.join(rbx_asset_own_path, glob_vars.rbx_asset_name_clean + ".obj")
                        blender_api_import_obj(obj_filepath)
                        blender_api_assets_new_material(rbx_asset_own_path, rbx_asset_items_dict, glob_vars.rbx_asset_name_clean)
                        blender_api_transparent_textures()
                        blender_api_assets_reposition()
                        blender_api_assets_remove_doubles()

                        if rbx_incl_cages:
                            cages_list = glob_vars.rbx_asset_sets_rbxm.get("Cages")
                            for cage in cages_list:
                                obj_filepath = os.path.join(rbx_asset_own_path, glob_vars.rbx_asset_name_clean + f"_{cage}.obj")
                                blender_api_import_obj(obj_filepath)
                                blender_api_assets_reposition(move_x_axis=5.0)









        
        ##### Character Import #####        
        if rbx_char == 'import' or rbx_char == 'my_avatar':  

            if rbx_char == 'my_avatar':
                ### Set username and user ID
                rbx_user_id = glob_vars.get_login_info()["user_id"]
                rbx_user_name = glob_vars.get_login_info()["user_name"]
                rbx_user_name_clean = replace_restricted_char(rbx_user_name)
                glob_vars.rbx_user_name_clean = rbx_user_name_clean  
                rbx_char_error = None
                glob_vars.rbx_char_error = rbx_char_error

            if rbx_char == 'import':    
                ### Set username and user ID
                rbx_username_or_id, username_field_is, rbx_char_error = check_username_field_and_extract_id(rbx_username_entered)
                if rbx_char_error == None:
                    if username_field_is != 'id':
                        rbx_user_name = rbx_username_or_id
                        rbx_user_id, rbx_char_error = get_user_id(rbx_user_name, headers)
                    else:
                        rbx_user_id = rbx_username_or_id
                        rbx_user_name, rbx_char_error = get_user_name(rbx_user_id, headers)
                    rbx_user_name_clean = replace_restricted_char(rbx_user_name)
                    glob_vars.rbx_user_name_clean = rbx_user_name_clean
            
            ### Create character folder
            if rbx_char_error == None:
                rbx_char_path = os.path.join(glob_vars.addon_path, glob_vars.rbx_import_main_folder, glob_vars.rbx_imported_char_fldr, rbx_user_name_clean)
                if not os.path.exists(rbx_char_path):
                    os.makedirs(rbx_char_path) 

            ### Get URL with all character hashes
            if rbx_char_error == None:
                rbx_usr_hsh_urls, rbx_char_error = get_user_hashes(rbx_user_id)
                dprint("rbx_usr_hsh_urls: ", rbx_usr_hsh_urls)

            if rbx_char_error == None: 
                avt_obj_hsh = rbx_usr_hsh_urls['obj']
                avt_mtl_hsh = rbx_usr_hsh_urls['mtl']
                avt_tex_hsh = rbx_usr_hsh_urls['textures']
                
                ### Get All URLs ###
                avt_mtl_url = get_cdn_url(avt_mtl_hsh)
                avt_obj_url = get_cdn_url(avt_obj_hsh)
                dprint("avt_mtl_url: ", avt_mtl_url)
                dprint("avt_obj_url: ", avt_obj_url)

                ### Add all Tex URL to list ###
                avt_tex_url = []
                for i in range(len(avt_tex_hsh)):
                    tmp_tex_url = get_cdn_url(avt_tex_hsh[i])
                    avt_tex_url.append(tmp_tex_url)  

                ### Download files ###
                if rbx_char_error == None:
                    data, rbx_char_error = download(avt_mtl_url,"mtl", "Avatar")
                    ### Save file ###
                    if rbx_char_error == None: 
                        rbx_mtl_file = os.path.join(rbx_char_path, glob_vars.rbx_user_name_clean + ".mtl")
                        save_to_file(rbx_mtl_file, data, "mtl", "Avatar")

                ### Download files ###       
                if rbx_char_error == None:
                    data, rbx_char_error = download(avt_obj_url,"Obj", "Avatar")
                    ### Save file ###
                    if rbx_char_error == None: 
                        rbx_obj_file = os.path.join(rbx_char_path, glob_vars.rbx_user_name_clean + ".obj")
                        save_to_file(rbx_obj_file, data, "Obj", "Avatar")


            ### Save textures
            if rbx_char_error == None:
                for i in range(len(avt_tex_url)):
                    data, rbx_char_error = download(avt_tex_url[i],"Texture", "Avatar")
                    if rbx_char_error == None:
                        rbx_tex_file = os.path.join(rbx_char_path, glob_vars.rbx_user_name_clean + '_tex-' + str(i) + ".png")
                        save_to_file(rbx_tex_file, data, "Texture", "Avatar")
                    else:
                        break

                    
            ### Write new Texture names into MTL ###
            if rbx_char_error == None:
                try:
                    with open(rbx_mtl_file, 'r', encoding='UTF-8') as f:
                        text = f.read()
                except:
                    rbx_char_error = "Error writing to MTL file"
                    glob_vars.rbx_char_error = rbx_char_error
                else:
                    with open(rbx_mtl_file, 'w', encoding='UTF-8') as f:
                        for i in range(len(avt_tex_hsh)):
                            text = text.replace(avt_tex_hsh[i], glob_vars.rbx_user_name_clean + '_tex-' + str(i) + ".png")
                        if "map_d" in text:
                            text = text.replace("map_d","") ## Remove transparency
                        if "map_Ka" in text:
                            text = text.replace("map_Ka","#map_Ka") ## Remove transparency
                        f.write(text)


                ### Start Character Import ###
                if not rbx_char_error:
                    blender_api_import_obj(rbx_obj_file)
                    blender_api_transparent_textures()
                    blender_api_assets_reposition()
                    blender_api_assets_remove_doubles()


            ### Split Accessories ###
            if rbx_split == True:
                if rbx_char_error == None:
                    
                    obj = context.active_object
                    i = 1
        
                    # Check if the selected object has any materials assigned to it
                    if not obj.material_slots:
                        rbx_char_error = "No materials assigned to selected object."
                        glob_vars.rbx_char_error = rbx_char_error
                    else:
                        bpy.ops.object.editmode_toggle()
                        bpy.ops.mesh.select_all(action='SELECT')
                        bpy.ops.mesh.separate(type='MATERIAL')
                        bpy.ops.object.editmode_toggle()
                        for selected in context.selected_objects:
                            if selected.name == obj.name:
                                # Deselect selected object
                                obj.select_set(False)
                            else:
                                # Set the new created object to active
                                context.view_layer.objects.active = selected
                                context.active_object.name = f"{obj.name}_Accessory_{i}"
                                i += 1
                        bpy.ops.object.select_all(action='DESELECT')



            






            
            
            
            
            

        return {'FINISHED'}


