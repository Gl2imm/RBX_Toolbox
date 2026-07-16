import os
import re
from .. import glob_vars


### Debug prints
DEBUG = False
dprint = lambda *args, **kwargs: print(*args, **kwargs) if DEBUG else None


def resolve_content_uri(value):
	"""Extract a URI string from an rbxm_reader Content property value.
	Content properties in the new reader return dicts like:
	  {"type": "Uri", "uri": "rbxassetid://123"}
	  {"type": "None"}
	Also handles plain strings (backwards compat) and None.
	Returns the URI string, or empty string if not available.
	"""
	if value is None:
		return ""
	if isinstance(value, dict):
		if value.get("type") == "Uri":
			return value.get("uri", "")
		return ""
	# Plain string (backwards compat or already resolved)
	return str(value)


## Sanitize a name for use as a filesystem path component / Blender datablock name ##
def replace_restricted_char(str: str = None):
	'''Sanitize a name so it is safe as a path component or Blender datablock name.

	Keeps only ASCII letters, digits and underscores. Every other character —
	spaces, punctuation, symbols (e.g. ♡) and non-ASCII letters — is replaced
	with "_"; consecutive replacements collapse into a single "_" and any
	leading/trailing "_" are trimmed for clean names. Surrounding whitespace is
	stripped first so Windows can't silently drop a trailing space/dot from a
	path component (which previously caused a created-dir vs file-open mismatch
	-> FileNotFoundError).'''
	if str is None:
		return
	# Replace every run of disallowed chars with one "_", then trim edge "_".
	new_str = re.sub(r'[^A-Za-z0-9_]+', '_', str.strip()).strip('_')
	# Guard against names that sanitize to nothing (e.g. fully non-ASCII).
	return new_str or "Unnamed"


## Pick a folder name that does not collide with existing folders ##
def unique_dir_name(parent_dir, base="Unnamed"):
	'''Return a folder name unique within `parent_dir`.

	If `parent_dir/base` is free, returns `base`; otherwise returns the next
	free `base_NN` ("Unnamed", "Unnamed_01", "Unnamed_02", ...). Used for the
	generic `replace_restricted_char` fallback so two differently-named assets
	that both sanitize to the same name don't overwrite each other's folder.

	Resolve this ONCE per asset (not per sanitize call); `replace_restricted_char`
	itself stays deterministic so dir-creation and file writes share one path.'''
	if not base:
		base = "Unnamed"
	candidate = base
	i = 1
	while os.path.exists(os.path.join(parent_dir, candidate)):
		candidate = f"{base}_{i:02d}"
		i += 1
	return candidate


## Remove rbxassetid:// part
def strip_rbxassetid(asset_str):
	""" Removes the 'rbxassetid://' prefix if present """
	asset_str = str(asset_str)
	prefix = "rbxassetid://"
	if asset_str.startswith(prefix):
		return asset_str[len(prefix):]
	else:
		asset_str = asset_str.split("=")[-1]
	return asset_str



# This asynchronous method is invoked as a separate coroutine from the main thread
async def renew_token(context):
	"""Refreshes Auth Token"""
	from ..oauth.lib.oauth2_client import RbxOAuth2Client
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



##### Create Folders #####
def create_and_open_folders(folder):
	if not os.path.exists(folder):
		os.makedirs(folder)
	os.startfile(folder)
	return



def cleanup_tmp_files(filenames:list, extension:str, folder_path:str = None):
	"""
	Deletes files from folder_path whose names match the list, with the given extension.
	If folder_path is not provided, defaults to tmp_rbxm.
	"""
	if folder_path is None:
		folder_path = os.path.join(glob_vars.addon_path, glob_vars.rbx_import_main_folder, 'tmp_rbxm')
	# make sure extension starts with "."
	if not extension.startswith("."):
		extension = "." + extension

	missing = []
	for name in filenames:
		file_path = os.path.join(folder_path, str(name) + extension)

		if os.path.exists(file_path):
			try:
				os.remove(file_path)
			except Exception as e:
				pass
				#dprint(f"❌ Could not delete {file_path}: {e}")
		else:
			missing.append(file_path)

	return


### Save Downloaded files
def save_to_file(file, data):
	"""Saving files."""
	rbx_imp_error = None
	try:
		with open(file, "wb") as f:
			f.write(data) 
	except Exception as e:
		rbx_imp_error = f"Error saving file. {e}"
		glob_vars.rbx_imp_error = rbx_imp_error
	return rbx_imp_error


##### Extract ID #####
def item_field_extract_id(rbx_item_field_entry):
	dprint("rbx_item_field_entry: ", rbx_item_field_entry)
	rbx_asset_id = None
	rbx_imp_error = None

	rbx_cat_url = "https://www.roblox.com/catalog/"
	rbx_bndl_url = "https://www.roblox.com/bundles/"
	rbx_store_url = "https://create.roblox.com/store/asset/"
	rbx_games_url = "https://www.roblox.com/games/"
	
	# Clean up input
	if rbx_item_field_entry.startswith("http://"):
		rbx_item_field_entry = rbx_item_field_entry.replace("http://", "https://")

	if rbx_cat_url in rbx_item_field_entry:
		rbx_asset_id = rbx_item_field_entry.replace(rbx_cat_url, "")
		rbx_asset_id = rbx_asset_id.split("/")[0]
	elif rbx_bndl_url in rbx_item_field_entry:
		rbx_asset_id = rbx_item_field_entry.replace(rbx_bndl_url, "")
		rbx_asset_id = rbx_asset_id.split("/")[0]
	elif rbx_store_url in rbx_item_field_entry:
		# Handle: https://create.roblox.com/store/asset/17253530672/rainbow-obby
		rbx_asset_id = rbx_item_field_entry.replace(rbx_store_url, "")
		rbx_asset_id = rbx_asset_id.split("/")[0]
		rbx_asset_id = rbx_asset_id.split("?")[0]  # Strip query params
	elif rbx_games_url in rbx_item_field_entry:
		# Handle: https://www.roblox.com/games/7016965078/mama-boss332s-Place
		rbx_asset_id = rbx_item_field_entry.replace(rbx_games_url, "")
		rbx_asset_id = rbx_asset_id.split("/")[0]
		rbx_asset_id = rbx_asset_id.split("?")[0]  # Strip query params
	elif rbx_item_field_entry.isdigit():
		rbx_asset_id = rbx_item_field_entry
	else:
		# If it's not a known URL format and not just digits, we might still try to strip basic non-digits or error out.
		# For now, let's assume if it's not a URL, it might be an ID if we strip headers.
		# But the original code was stricter. Let's stick to supporting specific URLs or digits.
		rbx_imp_error = "Error: Invalid item URL or ID"
		glob_vars.rbx_imp_error = rbx_imp_error

	if rbx_asset_id and not rbx_asset_id.isdigit():
		rbx_asset_id = None
		rbx_imp_error = "Error: extracted ID is not a number"
		glob_vars.rbx_imp_error = rbx_imp_error

	return rbx_asset_id, rbx_imp_error