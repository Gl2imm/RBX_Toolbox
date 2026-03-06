# ##### BEGIN GPL LICENSE BLOCK #####
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# ##### END GPL LICENSE BLOCK #####


import bpy, os, requests, json, zipfile, socket, time, threading, shutil
import rna_keymap_ui
import bpy.utils.previews
from bpy.types import PropertyGroup, Panel, Operator, AddonPreferences
from bpy.props import *
from subprocess import check_output

# Add-on info
bl_info = {
    "name": "Easy PBR",
    "author": "Monaime Zaim (CodeOfArt.com)",
    "version": (0, 9, 3),
    "blender": (2, 93, 0),
    "location": "Shader Editor > Properties > EPBR",
    "description": "PBR Shaders | Download | Setup | Mixing.",
    "warning": "Beta",
    "wiki_url": "",
    "tracker_url": "",
    "category": "Material"
    }
    
preview_collections = {}
download_threads = []
baking_queue = []
baking_op = None
addon_keymaps = []
addon_folder = os.path.dirname(__file__)

# Library paths to Ambient CG folders and files
class ACG_paths():
    
    def __init__(self, context):
        self.prefs = prefs(context)
        
    def lib_path(self):
        if not self.prefs:
            return ''
        return self.prefs.lib_path
    
    def previews_path(self):
        lib_path = self.lib_path()
        if not lib_path:
            return ''
        return os.path.join(lib_path, 'Previews')
    
    def pbr_tex_path(self):
        lib_path = self.lib_path()
        if not lib_path:
            return ''
        return os.path.join(lib_path, 'PBR_Textures')
    
    def lib_json_path(self):
        lib_path = self.lib_path()
        file_name = 'AmbientCG_lib.json'
        if not lib_path:
            return ''
        return os.path.join(lib_path, file_name)
    
# AmbientCG library dictionary
class ACG_library():
    
    def __init__(self, context):
        self.lib = None
        settings = context.scene.easy_pbr_settings
        if len(settings):
            self.lib = settings[0].acg_library
        
    def assets(self):
        assets = []
        if not self.lib:
            return assets
        assets = self.lib.get('Assets')
        if assets is None:
            return assets
        # exclude the missplaced substance assets
        try:
            assets = [i for i in assets if 'Substance' not in i]
        except:
            pass    
        return assets
    
    def categories(self):
        if not self.lib:
            return []
        return self.lib.get('Categories')
    
    def request_time(self):
        if not self.lib:
            return ''
        return self.lib.get('RequestTime')
    
    def resolutions(self, asset):
        if not self.lib:
            return []
        res = []
        try:
            res = list(self.lib['Assets'][asset]['Downloads'])
        except:
            pass
        return res
    
    def preview_link(self, asset, res):
        if not self.lib:
            return ''
        link = ''
        try:
            link = self.lib['Assets'][asset]['PreviewSphere'][res]
        except:
            pass
        return link
    
    def asset_link(self, asset, res):
        if not self.lib:
            return ''
        link = ''
        try:
            link = self.lib['Assets'][asset]['Downloads'][res]['RawDownloadLink']
        except:
            pass
        return link
    
    def asset_size(self, asset, res):
        if not self.lib:
            return ''
        size = 0
        try:
            size = self.lib['Assets'][asset]['Downloads'][res]['Size']
        except:
            pass
        return size
    
    def asset_weblink(self, asset):
        if not self.lib:
            return ''
        link = ''
        try:
            link = self.lib['Assets'][asset]['Weblink']
        except:
            pass
        return link
    
    def asset_releasedate(self, asset):
        if not self.lib:
            return ''
        date = ''
        try:
            date = self.lib['Assets'][asset]['AssetReleasedate']
        except:
            pass
        return date
    
    def asset_creation_method(self, asset):
        if not self.lib:
            return ''
        method = ''
        try:
            method = self.lib['Assets'][asset]['CreationMethodID']
        except:
            pass
        # Separate the words
        method = ''.join(' ' + x if x.isupper() else x for x in method).strip(' ')
        return method
    
    def asset_tags(self, asset):
        if not self.lib:
            return []
        tags = []
        tags_str = ''
        try:
            tags_str = self.lib['Assets'][asset]['Tags']
        except:
            pass
        # Separate the words into a list
        tags = tags_str.split(',')
        return tags
    
    def asset_filetype(self, asset, res):
        if not self.lib:
            return []
        filetype = ''
        try:
            filetype = self.lib['Assets'][asset]['Downloads'][res]['Filetype']
        except:
            pass
        return filetype
    
################################################################################
############################# General Utils ####################################
################################################################################
# Add-on Preferences
def prefs(context):
    addon = context.preferences.addons.get(__name__)
    if addon:
        return addon.preferences
    return None

# list of the available previews
def available_previews(context):
    assets = ACG_library(context).assets()
    if not assets:
        return []
    prevs_path = ACG_paths(context).previews_path()
    if not os.path.exists(prevs_path):
        return []
    avail = os.listdir(prevs_path)
    assets = [i.lower()+'.png' for i in assets]
    return [i for i in avail if i.lower() in assets]

# List of categories (enum)
def categories_enum(self, context):
    cats = ACG_library(context).categories()
    if cats:
        cats.sort() # sort alphabetically
        return [(i, i, '') for i in cats]
    return [('Empty', '__Empty__', '')]

# Enable the settings for Easy PBR
def enable_settings(context):
    settings = context.scene.easy_pbr_settings
    if not len(settings):
        settings.add()
        settings.update()

# Confirm that the path to the library is valid
def confirm_lib_path(path):
    if not path.strip():
        return False
    
    if not os.path.exists(path):
        return False
    
    elements = os.listdir(path)
    if not elements:
        return False
    
    necessary = ['AmbientCG_lib.json', 'PBR_Textures', 'Previews']    
    for i in necessary:
        if not i in elements:
            return False
        
    return True

# Load the dictionary when the folder selection changes
def update_dict(self, context):
    scn = context.scene
    path = self.lib_path    
    if not confirm_lib_path(path):
        return None
    
    settings = context.scene.easy_pbr_settings
    enable_settings(context)
    coll = settings[0]
        
    lib_json = os.path.join(path, "AmbientCG_lib.json")
    lib_dict = load_json_lib(lib_json)
    if not lib_dict:
        return None
    # load the library to memory (load to blend file)    
    for key in lib_dict:
        coll.acg_library[key] = lib_dict[key]
    # fill the search field (for minimizing the thumbnail generation)    
    filter = coll.epbr_shaders_filtering
    category = coll.epbr_categories
    if not filter.strip() and category != 'Empty':
        coll.epbr_shaders_filtering = category
    # setup the asset library
    set_epbr_asset_lib(context, path)
    return None        

# Load the json of the library (Convert from json to dict)
def load_json_lib(path):
    lib_dict = {}
    if not os.path.exists(path):
        print("Can't load the json lirary!")
        return lib_dict
    
    with open(path, 'r') as json_file:
        lib_dict = json.load(json_file)
    return lib_dict

# Get the index of a property in a group
def get_item_idx(items, name):
    for idx, item in enumerate(items):
        if item.name == name:
            return idx
    return None

# Delete the zip file
def delete_zip(file_path):
    if not os.path.exists(file_path):
        #print(file_path + " Zip file doesn't exists")
        return
    try:
        os.remove(file_path)
    except Exception as e:
        print('Error while deleting zip file:', e)
        
# Get the list of available resolutions
def get_tex_res(context, asset, loc):
    res = ['Empty']
    
    if loc == 'LOCAL':
        pbr_tex_path = ACG_paths(context).pbr_tex_path()
        if not pbr_tex_path:
            return res
        assets = os.listdir(pbr_tex_path)
        if not asset in assets:
            return res
        tex_path = os.path.join(pbr_tex_path, asset)
        avail = os.listdir(tex_path)
        res = avail if avail else res
    else:
        avail = ACG_library(context).resolutions(asset)
        res = avail if avail and avail != [''] else res
    return res

# Get the list of downloaded resolutions (enum)
def get_local_res_enum(self, context):
    tex = self.shaders_previews
    res = get_tex_res(context, tex, 'LOCAL')
    return [(i, i, '') for i in res]

# Get the list of available resolutions (enum)
def get_online_res_enum(self, context):
    tex = self.shaders_previews
    res = get_tex_res(context, tex, 'ONLINE')
    return [(i, i, '') for i in res]

# Get the list of downloaded resolutions (enum)
# For changing the resolution operator
def get_avail_res(self, context):
    asset = ''
    active_node = None
    ob = context.object
    mat = ob.active_material
    if mat.use_nodes:
        nodes = mat.node_tree.nodes
        if len(nodes):
            active_node = nodes.active
    if active_node:
        info = active_node.label.split()
        if len(info):
            asset = info[0]
    res = get_tex_res(context, asset, 'LOCAL')
    return [(i, i, '') for i in res]

# Get the list of available outputs
def get_node_outputs( context):
    types = ['VALUE', 'INT', 'BOOLEAN', 'VECTOR', 'RGBA']
    ob = context.object
    mat = ob.active_material
    nodes = mat.node_tree.nodes
    node = nodes.active
    if node is None:
        return []
    return [i.name for i in node.outputs if i.type in types]
    
def get_node_outputs_enum(self, context):
    outputs = get_node_outputs(context)
    return [(i, i, '') for i in outputs]

# Extract the downloaded zip file
def extract_zip(file_path):
    try:
        with zipfile.ZipFile(file_path) as compressed:
            dir = os.path.dirname(file_path)
            compressed.extractall(path = dir)
    except Exception as e:
        print('Error while extracting the zip file:', e)
    finally:
        delete_zip(file_path)
    
# Check if the texture is downloaded
def asset_downloaded(context, asset_name, res):
    resolutions = get_tex_res(context, asset_name, 'LOCAL')
    if resolutions == ['Empty']:
        #print('Empty')
        return False
    
    if not res in resolutions:
        #print(res, ' not in resolutions')
        return False
    
    pbr_tex_path = ACG_paths(context).pbr_tex_path()
    tex_path = os.path.join(pbr_tex_path, asset_name)
    asset = os.path.join(tex_path, res)
    textures = os.listdir(asset)
    if not textures:
        #print('No textures found')
        return False
    if len(textures) == 1:
        texture = textures[0]
        if texture.lower().endswith(".zip"):
            #print('only the zip file')
            return False
    return True

# Check if the active area is the shader editor
def check_area(context):
    space = context.space_data
    if not space.type == 'NODE_EDITOR':
        return False
    return space.tree_type == 'ShaderNodeTree'

# Give the asset a more readable name by separating the words
# names format: NAME + 3 Numbers + Sometimes a letter
def asset_pretty_name(ugly_name):
    if ugly_name == 'EMPTY' or not ugly_name.strip():
        return ugly_name
    s = ugly_name[-1:] if ugly_name[-1:].isalpha() else ''
    ugly_name = ugly_name[:-1] if s else ugly_name
    name = ugly_name[:-3]
    num = ugly_name[-3:]
    n = ''.join(' ' + x if x.isupper() else x for x in name).strip(' ')
    pretty_name = n + ' ' + num + ' ' + s
    return pretty_name
######################## Generating Thumbnails ########################
    
# Get the list of assets, applying the search filter
def assets_list(context, filter, loc):
    assets = ACG_library(context).assets()
    if not assets:
        return ['EMPTY']
    
    if filter.strip():
        assets = [i for i in assets if filter.lower() in i.lower()]
        
    if loc == 'LOCAL':
        pbr_tex_path = ACG_paths(context).pbr_tex_path()
        if os.path.exists(pbr_tex_path):
            available = os.listdir(pbr_tex_path)
            assets = [i for i in available if i in assets]
            
    if not assets:
        return ['EMPTY']
        
    assets.sort()
    return assets

# Generate shaders previews
def shaders_previews_enum(self, context):
    enum_items = []
    
    if context is None:
        return enum_items
    
    pcoll = preview_collections["shaders_previews"]
    if not pcoll.refresh and len(pcoll):
        return pcoll.shaders_previews
    
    previews_path = ACG_paths(context).previews_path()
    filter = self.epbr_shaders_filtering
    loc = self.epbr_tex_location
    assets = assets_list(context, filter, loc)
    images = available_previews(context)
    images = [i.lower() for i in images]
    
    no_prev_path = os.path.join(addon_folder, 'Images', 'NoPreview.png')
    no_prev_thumb = pcoll.get('NoPreview')
    if not no_prev_thumb:
        no_prev_thumb = pcoll.load('NoPreview', no_prev_path, 'IMAGE')
    
    for i , name in enumerate(assets):
        if name == 'EMPTY':
            filepath = os.path.join(addon_folder, 'Images', 'EMPTY.png')
        elif name.lower() + '.png' in images:
            filepath = os.path.join(previews_path, name + '.png')
        else:
            filepath = no_prev_path
        thumb = pcoll.get(name)
        if not thumb:
            if filepath == no_prev_path:
                thumb = no_prev_thumb
            else:
                thumb = pcoll.load(name, filepath, 'IMAGE')
        enum_items.append((name, name, "", thumb.icon_id, i))
    pcoll.shaders_previews = enum_items
    pcoll.refresh = ""
    return pcoll.shaders_previews

# Update the resolution when the previews changes
def update_preview(self, context):
    tex = self.shaders_previews
    local_res = get_tex_res(context, tex, 'LOCAL')
    self.epbr_local_res = local_res[0]
    online_res = get_tex_res(context, tex, 'ONLINE')
    self.epbr_online_res = online_res[0]
    return None

# Update the previews when the search field chenges
def update_shaders_previews(self, context):
    tex = self.shaders_previews
    filter = self.epbr_shaders_filtering
    loc = self.epbr_tex_location
    previews = ACG_paths(context).previews_path()
    assets = assets_list(context, filter, loc)
    
    try:
        refresh_previews()
    except Exception as e:
        print('Error in update_shaders_previews:', e)
    finally:
        items = [i.lower() for i in assets]
        if not tex.lower() in items:
            tex = assets[0]
        self.shaders_previews = tex
        
        local_res = get_tex_res(context, tex, 'LOCAL')
        self.epbr_local_res = local_res[0]
        online_res = get_tex_res(context, tex, 'ONLINE')
        self.epbr_online_res = online_res[0]
    return None

# Update the category
def update_category(self, context):
    cats = self.epbr_categories
    if not cats in ['Empty', '']:
        self.epbr_shaders_filtering = cats
    return None

# Refresh the previews:
def refresh_previews():
    pcoll = preview_collections["shaders_previews"]
    pcoll.refresh = 'Refresh Now'
    pcoll.update()
    
# Rload the previews:
def reload_previews():
    pcoll = preview_collections['shaders_previews']
    pcoll.clear()
    pcoll.refresh = 'Refresh Now'
    pcoll.update()
    
################################################################################
########################## Asset Browser Utils #################################
################################################################################

# add Easy PBR as an asset library
# TODO
# There is probably a better way for adding a library
def set_epbr_asset_lib(context, path):
    # make sure we are using Blender 3.0 or above
    if bpy.app.version < (3, 0, 0):
        return
    libraries = context.preferences.filepaths.asset_libraries
    asset_lib = libraries.get('Easy PBR')
    if asset_lib is not None:
        asset_lib.path = path
    else:
        asset_lib = None
        bpy.ops.preferences.asset_library_add(directory = path)
        for lib in libraries:
            if lib.path == path and lib.name == '':
                lib.name = 'Easy PBR'
                asset_lib = lib
                break
    # just in case if we want to do something with the library
    return asset_lib

# load and  mark all the EPBR shaders in the current blend file as assets
def mark_all_as_assets(context):
    previews = available_previews(context)
    previews = [i.lower() for i in previews]
    previews_path = ACG_paths(context).previews_path()
    
    override = context.copy()
    materials = bpy.data.materials
    assets = assets_list(context, '', 'LOCAL') # downloaded assets
    len_assets = len(assets)
    #mts  = [i.name for i in materials if i.asset_data is None]
    assets = [i for i in assets if i not in materials]
    if not assets:
        print('All the materials are already loaded and marked!')
        return
    
    print('Total downloaded assets: ', len_assets)
    print('Total assets to load: ', len(assets))
    materials_loaded, materials_marked, thumbnails_loaded = (0,0,0)
    for asset in assets:
        res = get_tex_res(context, asset, 'LOCAL')
        if 'Empty' in res:
            print('Empty folder for the asset: ', asset)
            continue
        # get the resolutions of the downloaded asset only
        res = [i for i in res if asset_downloaded(context, asset, i)]
        if not len(res):
            print('Empty folder for the asset: ', asset)
            continue
        res.sort()
        # create the material with the lowest resolution available to save space
        try:
            mat = add_pbr_mat(context, asset, res[0], True)
        except Exception as e:
            print('Error while loading:', asset)
            print(e)
            continue
        materials_loaded += 1
        # create the asset
        mat.asset_mark()
        materials_marked += 1
        # add the tags
        tags = ACG_library(context).asset_tags(asset)
        for tag in tags:
            mat.asset_data.tags.new(tag,  skip_if_exists = True)
        # the author (AmbientCG)
        mat.asset_data.author = 'AmbientCG.com'
        # generate or load the thumbnail
        override['id'] = mat
        if asset.lower() + '.png' in previews:
            filepath = os.path.join(previews_path, asset + '.png')
            # load the thumbnail
            bpy.ops.ed.lib_id_load_custom_preview(override,filepath=filepath)
            thumbnails_loaded += 1
        else:
            print('Missing thumbnail for the asset:', asset)
            # generate a new thumbnail if not present
            # generating a new thumbnail in the background crashs Blender
            #bpy.ops.ed.lib_id_generate_preview(override)
    print('Loaded Materials: ', materials_loaded)
    print('Marked Materials: ', materials_marked)
    print('Loaded Thumbnails: ', thumbnails_loaded)
            
# Load all the downloaded shaders in the background, then mark them as assets
# To be used in the Asset Browser
def add_all_as_assets(blend_file, reload = False):
    start_time = int(time.time())
    blender = bpy.app.binary_path
    script_file = 'reload_all_assets.py' if reload else 'add_all_assets.py'
    output = check_output([blender,
                           blend_file,
                           '--background',
                           '--python-text',
                           script_file])
    
    print('-----------------------------------------------------------------')
    print('---------------  Loading EasyPBR Shaders Started  ---------------')
    print('-----------------------------------------------------------------')
    
    print(output.decode("utf-8"))
    end_time = int(time.time())
    total_time = end_time - start_time
    print('The operation took: ', total_time, ' Seconds')
    
    print('-----------------------------------------------------------------')
    print('---------------  Loading EasyPBR Shaders Finished  --------------')
    print('-----------------------------------------------------------------')

################################################################################
############################# Download Utils ###################################
################################################################################

# Monitor the downloads, cleanup downloaded items, refresh the UI
def monitor_downloads():
    
    interval = 0.50 # execute every x seconds, 2 times a second in our case
    update_progress = False
    if not hasattr(bpy, 'context'):
        return 2
    
    scn = bpy.context.scene
    epbr_settings = scn.easy_pbr_settings
    if not len(epbr_settings):
        return 2
    
    settings = epbr_settings[0]
    downloads = settings.downloads
    
    if not len(downloads):
        return 1
    
    for area in bpy.context.screen.areas:
        if not area.type == 'NODE_EDITOR':
            continue
        if area.spaces[0].tree_type == "ShaderNodeTree":
            update_progress = True
            area.tag_redraw()
    
    global download_threads
    
    for dwn in downloads:
        try:
            thread = get_asset_thread(dwn.name)
            idx = get_item_idx(downloads, dwn.name)
            
            if thread is None:
                delete_zip(dwn.file_path)
                if idx is not None:
                    downloads.remove(idx)
                continue
            
            if thread.is_alive():
                if update_progress:
                    dwn.progress = int(thread.progress)
                continue
            
            dwn.alive = False
            
            if thread.stop or thread.progress == 100:
                delete_zip(dwn.file_path)
                thread.join() # not sure if necessary with the current implementation
                download_threads.remove(thread)
                if idx is not None:
                    downloads.remove(idx)
        except Exception as e:
            print('Error while monitoring the downloads:', e)
            continue
    return interval

# Check for an active internet connection
def check_internet(host="8.8.8.8", port=53, timeout=2):
    try:
        socket.setdefaulttimeout(timeout)
        socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((host, port))
        return True
    except socket.error as e:
        #print(e)
        pass
        return False
    
# get asset's thread
def get_asset_thread(asset):
    for thread in download_threads:
        if thread.name == asset:
            return thread
    return None

# Request a page from AmbientCG.com, using it's API (V1)
# If the request was successful, It will return a Response
# with the list of requested assets in json format
def request_page(assets_per_page, page_number, timeout):
    url = 'https://ambientcg.com/api/v1/full_json'
    params = {
        'type': 'Material',
        'include':'imageData,downloadData',
        'limit': str(assets_per_page),
        'offset': str(assets_per_page * page_number) 
        }
    headers = {'User-Agent' : 'EasyPBR'}
    r = requests.get(url, params=params, headers=headers, timeout = timeout)
    if not r.status_code == 200:
        print("Can't download, Code: " + str(r.status_code))
        return None
    return r


# Get the total number of assets using the API V2
# It's not possible to get the total number using V1
def get_assets_number():
    num = 0
    url = 'https://ambientcg.com/api/v2/full_json'
    params = {'type': 'Material', 'limit': '1'}
    headers = {'User-Agent' : 'EasyPBR'}
    try:
        r = requests.get(url, params=params, headers=headers)
        if not r.status_code == 200:
            print("Can't download, Code: " + str(r.status_code))
            return num
        lib = r.json()
        num = int(lib['numberOfResults'])
    except Exception as e:
        print('Error in "get_asset_number":', e)
    return num


# Download the json file of the full PBR Textures library, from AmbientCG.com
def update_lib(timeout, file_path, backup_file_path, assets_number):
    # create a backup file
    shutil.copy2(file_path, backup_file_path)
    
    assets_per_page = 100 #100 is the max assets per-page in AmbientCG
    assets = {'Assets': {}, 'Categories': [], 'RequestTime': ''}
    thread = get_asset_thread('Library')
    #calculate the number of pages
    pages_number = (assets_number // assets_per_page)
    if assets_number % assets_per_page:
        pages_number += 1
    # download
    try:
        for i in range(pages_number):
            if thread is not None and thread.stop:
                return
            req = request_page(assets_per_page, i, timeout)
            lib = req.json()
            assets['Assets'] |= lib['Assets']
            # Update the progress
            thread = get_asset_thread('Library')
            if thread is not None:
                thread.progress = (i+1)/pages_number* 100
    except Exception as e:
        print('Error while downloading the library:', e)            
    # Extracting the categories
    for i in assets['Assets']:
        # Ignore the missplaced Substance assets
        if 'Substance' in i:
            continue
        # Delete the numerotation, then the duplicates
        cat = i[:-3]
        if cat[-1:] == '0':
            cat = cat[:-1]
        if cat not in assets['Categories']:
            assets['Categories'].append(cat)
    assets['RequestTime'] = lib['RequestTime']
    # Save the file
    with open(file_path, 'w') as json_file:
        json.dump(assets, json_file, indent=5)
    # Load the library
    try:
        lib_path = prefs(bpy.context).lib_path
        prefs(bpy.context).lib_path = lib_path
    except Exception as e:
        print('Error while loading the library:', e)

# Download an asset from AmbientCG.com        
def download_asset(asset, res, link, filepath, timeout):
    prog = 0
    with open(filepath, "wb") as f:
        try:
            thread = get_asset_thread(asset+res)
            response = requests.get(link, stream=True, timeout = timeout)
            # session seems to be a little bit faster
            #session = requests.Session()
            #response = session.get(link, stream=True, timeout = timeout)
            total_length = response.headers.get('content-length')
            if not total_length:
                print('Error while downloading', asset, ':', "Empty Response.")
                return
            
            dl = 0
            total_length = int(total_length)
            # TODO a way for calculating the chunk size
            for data in response.iter_content(chunk_size = 4096):
                if thread is not None and thread.stop:
                    response.close()
                    break
                dl += len(data)
                f.write(data)
                
                if thread is not None:
                    prog = int(100 * dl / total_length)
                    thread.progress = prog
                
        except Exception as e:
            print('Error while downloading', asset, ':', e)
    if os.path.exists(filepath) and prog == 100:
        extract_zip(filepath)

# Download the missing previews of the assets
def download_previews(assets, links, total, prevs_path, timeout):
    thread = get_asset_thread('Previews')
    prog = total - len(links)
    for i, link in enumerate(links):
        if thread is not None and thread.stop:
            return
        if not link:
            print('Download link missing for ' + assets[i])
            continue
        try:
            response = requests.get(link, timeout = timeout)
            total_length = response.headers.get('content-length')
            if not total_length:
                print("Downloading the Previews Failed: Empty Response.")
                return
            filepath = os.path.join(prevs_path, assets[i]+'.png')
            with open(filepath, "wb") as f:
                f.write(response.content)
        except Exception as e:
            print('Error while downloading the previews:', e)
            return
        prog += 1
        
        if thread is not None:
            thread.progress = prog/total* 100
        else: # in the first iteration the thread isn't added yet
            thread = get_asset_thread('Previews')
    if len(assets):
        reload_previews()
                
################################################################################
############################# Shader Utils #####################################
################################################################################

# Find recursively all the nodes connected to the right of a node
class EPBR_notr:
    def __init__(self):
        self.nodes = []
    
    def find(self, node):
        # list of the connected nodes to the outputs of the node
        nodes = [l.to_node for o in node.outputs for l in o.links]
        # add to the main list
        self.nodes.extend(nodes)
        # next nodes
        for n in nodes:
            self.find(n)
        
    def get_nodes(self, node):
        self.find(node)
        # remove the duplicates
        nodes = list(dict.fromkeys(self.nodes))
        return nodes

# indexs of the sockets in the principled node
def principled_indexs():
    # for backward compatibility
    if bpy.app.version >= (3, 0, 0):
        idx = {
            'Color' : 0,
            'Metallic' : 6,
            'Alpha' : 21,
            'Roughness' : 9,
            'Emission' : 19,
            'Normal' : 22
        }
    else:
        idx = {
            'Color' : 0,
            'Metallic' : 4,
            'Alpha' : 19,
            'Roughness' : 7,
            'Emission' : 17,
            'Normal' : 20
        }
    return idx

def asset_channels(context, asset_name = '', res = ''):
    #(channel's name : [naming convention, image path, default value, socket type, image name])
    all_maps = {
        'AO' : ['_ambientocclusion.', '', (1.0, 1.0, 1.0, 1.0), 'NodeSocketColor', ''],
        'Color' : ['_color.', '', (0.8, 0.8, 0.8, 1.0), 'NodeSocketColor', ''],
        'Metallic' : ['_metalness.', '', 0.0, 'NodeSocketFloat', ''],
        'Roughness' : ['_roughness.', '', 0.5, 'NodeSocketFloat', ''],
        'Emission' : ['_emission.', '', (0.0, 0.0, 0.0, 1.0), 'NodeSocketColor', ''],
        'Alpha' : ['_opacity.', '', 1.0, 'NodeSocketFloat', ''],
        'Normal' : ['_normalgl.', '', (0.5, 0.5, 1.0, 1.0),'NodeSocketColor', ''],
        'Displacement' : ['_displacement.', '', 0.5, 'NodeSocketFloat', ''],
    }
    maps = {}
    if not asset_name:
        return all_maps
    tex_path = ACG_paths(context).pbr_tex_path()
    asset_path = os.path.join(tex_path, asset_name, res)
    if not os.path.exists(asset_path):
        return all_maps
    # Assigning the images paths
    images = os.listdir(asset_path)
    for img in images:
        for map in all_maps:
            if all_maps[map][0] in img.lower():
                all_maps[map][1] = os.path.join(asset_path, img)
                all_maps[map][4] = img
                maps[map] = all_maps[map]
                break
    # load the roughness of the surface inperfections assets
    special_cases = ['SurfaceImperfections', 'Scratches', 'Smear']
    for i in special_cases:
        if not i in asset_name:
            continue
        rough = maps.get('Roughness')
        if not rough:
            for img in images:
                if '_var1' in img.lower():
                    all_maps['Roughness'][1] = os.path.join(asset_path, img)
                    maps['Roughness'] = all_maps['Roughness']
                    break
    return maps

# get active output node:
def get_active_output_node(nodes):
    outputs = [n for n in nodes if n.type == 'OUTPUT_MATERIAL']
    if not outputs:
        return None
    for out in outputs:
        if out.is_active_output:
            return out

# Clear the output links of a node-group
def clear_node_outputs(links, node):
    for output in node.outputs:
        for link in output.links:
            links.remove(link)
            
# Clear the input links of a node-group
def clear_node_inputs(links, node):
    for input in node.inputs:
        # skip the factor input of the "mix epbr shaders" node
        if input.name == 'Factor':
            continue
        for link in input.links:
            links.remove(link)
            
# Detect the slot(s) in the mix shaders node
# Return the connected nodes
def mix_slots(context, mix):
    slots = [None, None]
    names = ['EPBR_Shader', 'EPBR_Mix_Shaders']
    channels = asset_channels(context)
    inputs = mix.inputs
    # check the first slots
    for channel in channels:
        input = inputs.get(channel + '1')
        if not input:
            continue
        links = input.links
        if len(links):
            n1 = links[0].from_node 
            for name in names:                    
                if name in n1.name:
                    slots[0] = n1
                    break
    # check the second slots
    for channel in channels:
        input = inputs.get(channel + '2')
        if not input:
            continue
        links = input.links
        if len(links):
            n2 = links[0].from_node 
            for name in names:                    
                if name in n2.name:
                    slots[1] = n2
                    break
    return slots

# Invert mix-node's input links
def invert_mix_links(context, links, mix_node):
    channels = asset_channels(context)
    inputs = mix_node.inputs
    for channel in channels:
        from_socket1, from_socket2 = (None, None)
        input1 = inputs.get(channel + '1')
        input2 = inputs.get(channel + '2')
        if input1:
            in_links = input1.links
            if len(in_links):
                from_socket1 = in_links[0].from_socket
                links.remove(in_links[0])
        if input2:
            in_links = input2.links
            if len(in_links):
                from_socket2 = in_links[0].from_socket
                links.remove(in_links[0])
        if from_socket1 and input2:
            links.new(from_socket1, input2)
        if from_socket2 and input1:
            links.new(from_socket2, input1)

# Create a new node group for a PBR Shader
def add_pbr_ng(context, asset_name, res, reload):
    channels = asset_channels(context, asset_name, res)
    node_groups = bpy.data.node_groups
    images = bpy.data.images
    ao, color = (None, None)
    
    pbr_ng = node_groups.new(asset_name, 'ShaderNodeTree')
    
    nodes = pbr_ng.nodes
    links = pbr_ng.links
    loc = [0.0, 0.0]
    x_margine, y_margine = (400.0, 50.0)
        
    #Adding new nodes
    #Inputs
    group_input = nodes.new('NodeGroupInput')
    group_input.name = 'Input'    
    group_input.location = loc
    
    pbr_ng.inputs.new('NodeSocketVectorXYZ', 'Coord')
    
    group_output = nodes.new('NodeGroupOutput')
    group_output.name = 'Output'
    
    loc[0] += x_margine
    img_y_loc = 0
    for i, channel in enumerate(channels):
        # Node_group outputs
        x, img_path, value, socket_type, img_name = channels[channel]
        pbr_ng.outputs.new(socket_type, channel)
        group_output.inputs[i].default_value = value
        if socket_type == 'NodeSocketFloat':
            pbr_ng.outputs[i].min_value = 0.0
            pbr_ng.outputs[i].max_value = 1.0
        # Images for the channels
        image = images.get(img_name)
        if not image or reload:
            image = images.load(img_path)
        tex_img = nodes.new(type = 'ShaderNodeTexImage')
        tex_img.image = image
        tex_img.hide = True
        tex_img.name =  'EPBR_Image'
        tex_img.label =  channel
        tex_img.location = (loc[0], img_y_loc)
        links.new(group_input.outputs[0], tex_img.inputs[0])
        links.new(tex_img.outputs[0], group_output.inputs[i])
        img_y_loc -= y_margine
        if channel != 'Color':
            tex_img.image.colorspace_settings.name = 'Non-Color'
        if channel == 'Color':
            color = tex_img
        if channel == 'AO':
            ao = tex_img
    loc[0] += x_margine
    # AO Multiplier
    if ao and color:
        ao_mult = nodes.new(type ="ShaderNodeMixRGB")
        ao_mult.name = 'AO Multiply'
        ao_mult.blend_type = 'MULTIPLY'
        ao_mult.hide = True
        ao_mult.inputs[0].default_value = 1.0
        ao_mult.inputs[2].default_value = [1.0, 1.0, 1.0, 1.0]
        ao_mult.location = (loc[0], -50.0)
        # group input
        pbr_ng.inputs.new('NodeSocketFloat', 'AO')
        pbr_ng.inputs['AO'].default_value = 1.0
        pbr_ng.inputs['AO'].min_value = 0.0
        pbr_ng.inputs['AO'].max_value = 1.0
        # links    
        links.new(group_input.outputs['AO'], ao_mult.inputs[0])
        links.new(color.outputs[0], ao_mult.inputs[1])
        links.new(ao.outputs[0], ao_mult.inputs[2])
        links.new(ao_mult.outputs[0], group_output.inputs['Color'])
    loc[0] += x_margine
    group_output.location = loc
    # Links
    return pbr_ng

# Create a new mix PBR Shaders node-group
def add_mix_pbr_ng(context):
    channels = asset_channels(context)
    node_groups = bpy.data.node_groups
    mix_ng = node_groups.new('EPBR Mix Shaders', 'ShaderNodeTree')
    
    nodes = mix_ng.nodes
    links = mix_ng.links
    loc = [0.0, 0.0]
    x_margine, y_margine = (400.0, 0.0)
        
    #Adding new nodes
    #Inputs
    group_input = nodes.new('NodeGroupInput')
    group_input.name = 'Input'    
    group_input.location = loc
    #Outputs
    group_output = nodes.new('NodeGroupOutput')
    group_output.name = 'Output'
    group_output.location =  [800, loc[1]]
    
    fac = mix_ng.inputs.new('NodeSocketFloat', 'Factor')
    fac.min_value = 0.0
    fac.max_value = 1.0
    
    for channel in channels:
        if channel == 'AO':
            continue
        
        x, img_path, value, socket_type, img_name = channels[channel]
        # mix node
        mix = nodes.new(type ="ShaderNodeMixRGB")
        mix.name = 'Mix ' + channel
        mix.blend_type = 'MIX'
        mix.hide = True
        mix.inputs[0].default_value = 0.0
        mix.location = (loc[0] + x_margine, y_margine)
        # math node
        fac_name = channel + ' Factor' 
        math = nodes.new(type ="ShaderNodeMath")
        math.operation = 'MULTIPLY'
        math.name = fac_name
        math.location = (mix.location[0], mix.location[1] - 40)
        math.hide = True
        links.new(group_input.outputs['Factor'], math.inputs[0])
        links.new(math.outputs[0], mix.inputs[0])
        #outputs
        mix_ng.outputs.new(socket_type, channel)
        group_output.inputs[channel].default_value = value
        if socket_type == 'NodeSocketFloat':
            mix_ng.outputs[channel].min_value = 0.0
            mix_ng.outputs[channel].max_value = 1.0
        links.new(mix.outputs[0], group_output.inputs[channel])
        #inputs
        ch = mix_ng.inputs.new('NodeSocketFloat', fac_name)
        mix_ng.inputs[fac_name].min_value = 0.0
        mix_ng.inputs[fac_name].max_value = 1.0
        mix_ng.inputs[fac_name].default_value = 1.0
        links.new(group_input.outputs[fac_name], math.inputs[1])
        for i in [1, 2]:
            name = channel + str(i)
            ch = mix_ng.inputs.new(socket_type, name)
            ch.default_value = value
            if socket_type == 'NodeSocketFloat':
                ch.min_value = 0.0
                ch.max_value = 1.0
            links.new(group_input.outputs[name], mix.inputs[i])
        y_margine -= 80
    return mix_ng

# Add the Shader as a new material
def add_pbr_mat(context, asset, res, reload):
    preferences = prefs(context)
    loc = [0.0, 0.0]
    x_margine = 500
    
    # add a new material
    mat = bpy.data.materials.new(asset)
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    
    # delete all the nodes, start from scratch
    mat.node_tree.nodes.clear()
    
    # Texture coordinates node
    tex_coord = nodes.new(type = 'ShaderNodeTexCoord')
    tex_coord.name = 'Coordinates'
    tex_coord.location = loc
    loc[0] += x_margine
    
    # Mapping node
    mapping = nodes.new(type = 'ShaderNodeMapping')
    mapping.name = 'Mapping'
    mapping.location = loc
    loc[0] += x_margine
    
    # asset node group
    ng = add_pbr_ng(context, asset, res, reload)
    asset_node = mat.node_tree.nodes.new(type="ShaderNodeGroup")
    asset_node.node_tree = ng
    asset_node.name = 'EPBR_Shader'
    asset_node.label = asset + ' ' + res
    asset_node.location = loc
    if preferences.custom_node_col:
        asset_node.use_custom_color = True
        asset_node.color = preferences.shader_node_col
    
    # principled node
    principled = nodes.new(type = 'ShaderNodeBsdfPrincipled')
    principled.name = 'Principled'
    loc[0] += x_margine
    principled.location = loc
    
    # material output
    output = nodes.new(type = 'ShaderNodeOutputMaterial')
    output.name = 'Output'
    loc[0] += x_margine
    output.location = loc
    
    # connect the loaded maps to the principled node
    connect_ng_principled(nodes, links, asset_node, principled, output)
    
    #links
    links.new(tex_coord.outputs[2], mapping.inputs[0])
    links.new(mapping.outputs[0], asset_node.inputs[0])
    links.new(principled.outputs[0], output.inputs[0])
    
    # assigning the material to the active object
    ob = context.object
    if ob is not None:
        ob.data.materials.append(mat)
    return mat
    
# Add the Shader as a new node group
def add_pbr_group(context, mat, asset, res, reload):
    preferences = prefs(context)
    # make sure that we can use the nodes
    mat.use_nodes = True
    
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    # find the principled node (if present)
    principled = None
    for node in nodes:
        if node.type == 'BSDF_PRINCIPLED':
            principled = node
            break
    # asset node group
    ng = add_pbr_ng(context, asset, res, reload)
    asset_node = mat.node_tree.nodes.new(type="ShaderNodeGroup")
    asset_node.node_tree = ng
    asset_node.name = 'EPBR_Shader'
    asset_node.label = asset + ' ' + res
    if preferences.custom_node_col:
        asset_node.use_custom_color = True
        asset_node.color = preferences.shader_node_col
    
    # node location
    if principled:
        asset_node.location[0] = principled.location[0] - 600
        asset_node.location[1] = principled.location[1]
    else:    
        asset_node.location = (0.0, 0.0)
    # Select the newly added node    
    for node in nodes:
        node.select = False
    asset_node.select = True        

# connect an EPBR-node-group to principled node
def connect_ng_principled(nodes, links, ng, principled, out):
    x_margine = 300.0
    loc = list(ng.location)
    # Prepare the nodes
    clear_node_outputs(links, ng)
    clear_node_inputs(links, principled)
    indexs = principled_indexs()
    # Connect with the Principled node
    for output in ng.outputs:
        if output.name == 'Normal':
            continue
        idx = indexs.get(output.name)
        if idx is None:
            continue
        links.new(output, principled.inputs[idx])        
    # Connect the Normal map node
    normal_node = None
    normal_out = ng.outputs.get('Normal')
    if normal_out:
        normal_node = nodes.get('EPBR_Normal')
        if normal_node:
            if normal_node.type != 'NORMAL_MAP':
                normal_node = None
        if not normal_node:
            normal_node = nodes.new(type="ShaderNodeNormalMap")
            normal_node.name = 'EPBR_Normal'
            normal_node.label = 'Normal Map'
        loc[0] += x_margine
        loc[1] -= 450
        normal_node.location = loc
        # links
        links.new(normal_out, normal_node.inputs[1])
        if not normal_node.outputs[0].is_linked:
            links.new(normal_node.outputs[0], principled.inputs[indexs.get('Normal')])
    arrange_bump_nodes(nodes, links, normal_node, principled)    
    # Displacement node
    disp_out = ng.outputs.get('Displacement')
    if not out or not disp_out:
        return
    disp_node = None
    if len(out.inputs[2].links):
        if out.inputs[2].links[0].from_node.type == 'DISPLACEMENT':
            disp_node = out.inputs[2].links[0].from_node
    if not disp_node:
        disp_node = nodes.new(type='ShaderNodeDisplacement')
        disp_node.name = 'Displacements'
    links.new(disp_node.outputs[0], out.inputs[2])
    disps = [d for d in nodes if 'EPBR_mix_disp' in d.name and d.type == 'MIX_RGB']
    free_disps = [d for d in disps if not d.inputs[1].is_linked]
    if len(disps) and not len(free_disps):
        mix_disp = mix_disp_node(nodes)
        free_disps.append(mix_disp)
    disp_in = free_disps[0].inputs[1] if len(free_disps) else disp_node.inputs[0]
    links.new(disp_out, disp_in)
    arrange_disp_nodes(nodes, links, disp_node, principled, out)

# Mix two EPBR shaders
def mix_pbrs(context, mat, ng1, ng2, mix_node):
    preferences = prefs(context)
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    channels = asset_channels(context)
    # mix node location
    mix_loc = [0.0, 0.0]
    if ng1 and ng2:
        mix_loc[0] = max(ng1.location[0], ng2.location[0]) + 250.0
        mix_loc[1] = max(ng1.location[1], ng2.location[1])
    elif ng1 and not ng2:
        mix_loc[0] = ng1.location[0] + 250
        mix_loc[1] = ng1.location[1]
    # mix node
    if not mix_node:
        mix_ng = add_mix_pbr_ng(context)
        mix_node = mat.node_tree.nodes.new(type="ShaderNodeGroup")
        mix_node.node_tree = mix_ng
        mix_node.name = 'EPBR_Mix_Shaders'
        mix_node.label = 'EPBR Mix Shaders'
        if preferences.custom_node_col:
            mix_node.use_custom_color = True
            mix_node.color = preferences.mix_node_col
    else:
        clear_node_inputs(links, mix_node)
    # Links
    #first node_group
    if ng1:
        mix_node.location = mix_loc
        clear_node_outputs(links, ng1)
        for output in ng1.outputs:
            input = mix_node.inputs.get(output.name + '1')
            if not input:
                continue
            links.new(output, input)
    
    # second node_group
    if ng2:
        clear_node_outputs(links, ng2)
        for output in ng2.outputs:
            input = mix_node.inputs.get(output.name + '2')
            if not input:
                continue
            links.new(output, input)

# find the principled node using four methods
def get_principled_node(nodes):
    # 1st method, using the active output node
    output = get_active_output_node(nodes)
    if output is not None:
        if output.inputs[0].is_linked:
            node = output.inputs[0].links[0].from_node
            if node.type == 'BSDF_PRINCIPLED':
                return node
    # 2nd method, using the normal_node
    normal_node = nodes.get('EPBR_Normal')
    if normal_node:
        for link in normal_node.outputs[0].links:
            node = link.to_node
            if node.type == 'BSDF_PRINCIPLED':
                return node
    # 3rd method, using the bump nodes
    bumps = [n for n in nodes if 'EPBR_Bump' in n.name and n.type == 'BUMP']
    for bump in bumps:
        for link in bump.outputs[0].links:
            node = link.to_node
            if node.type == 'BSDF_PRINCIPLED':
                return node
    # 4th method, choose an arbitrary principled node
    for node in nodes:
        if node.type == 'BSDF_PRINCIPLED':
            return node
    return None
            
# Add a bump-node
def connect_as_bump(node_output, nodes, links):
    bumps = [n for n in nodes if 'EPBR_Bump' in n.name and n.type == 'BUMP']
    free_bumps = [n for n in bumps if not n.inputs[2].is_linked]
    if len(free_bumps):
        bump_node = free_bumps[0]
    else:
        bump_node = nodes.new(type="ShaderNodeBump")
        bump_node.name = 'EPBR_Bump'
        bump_node.label = 'Bump Map'
    links.new(node_output, bump_node.inputs[2])
    normal_node = nodes.get('EPBR_Normal')
    principled = get_principled_node(nodes)
    arrange_bump_nodes(nodes, links, normal_node, principled)
    
# Arrange and connect the bump nodes
def arrange_bump_nodes(nodes, links, normal_node, principled):
    x_margine = 300.0
    bumps = [n for n in nodes if 'EPBR_Bump' in n.name and n.type == 'BUMP']
    # get the intial location
    loc = [0.0, 0.0]
    if normal_node:
        loc = list(normal_node.location)
    elif principled:
        loc[0] = principled.location[0] - x_margine
        loc[1] = principled.location[1] - 450.0
    # arrange the bump nodes
    # for backward compatibility
    nor_idx = 5 if bpy.app.version < (3, 2, 0) else 3
    for i, bump in enumerate(bumps):
        loc[0] += x_margine
        if i == 0 and normal_node:
            links.new(normal_node.outputs[0], bump.inputs[nor_idx])
        elif i in range(1, len(bumps)):
            links.new(bumps[i-1].outputs[0], bump.inputs[nor_idx])
        if i == len(bumps)-1 and principled:
            idxs = principled_indexs()
            links.new(bump.outputs[0], principled.inputs[idxs.get('Normal')])
        bump.location = loc
    #move the principled node and all the nodes connected to it
    if principled:
        principled_old_x = principled.location[0]
        principled.location[0] = loc[0] + x_margine
        # nodes on the right
        notr = EPBR_notr().get_nodes(principled)
        x_offset = principled.location[0] - principled_old_x
        for n in notr:
            n.location[0] += x_offset
            
# the mix displacements node
def mix_disp_node(nodes):
    mix_node = nodes.new(type ="ShaderNodeMixRGB")
    mix_node.name = 'EPBR_mix_disp'
    mix_node.blend_type = 'ADD'
    mix_node.inputs[0].default_value = 0.25
    mix_node.inputs[1].default_value = [0,0,0,1]
    mix_node.inputs[2].default_value = [0,0,0,1]
    return mix_node
    
        
# Add a mix displacements node
def connect_as_disp(node_output, nodes, links):
    disps = [d for d in nodes if 'EPBR_mix_disp' in d.name and d.type == 'MIX_RGB']
    free_disps = [d for d in disps if not d.inputs[2].is_linked]
    if len(free_disps):
        mix_node = free_disps[0]
    else:
        mix_node = mix_disp_node(nodes)
        
    links.new(node_output, mix_node.inputs[2])
    
    disp_node = None
    output = get_active_output_node(nodes)
    if output is not None:
        if output.inputs[2].is_linked:
            node = output.inputs[2].links[0].from_node
            if node.type == 'DISPLACEMENT':
                disp_node = node
    if not disp_node:
        disp_node = nodes.new(type='ShaderNodeDisplacement')
        disp_node.name = 'Displacements'
        if output:
            links.new(disp_node.outputs[0], output.inputs[2])
    if not len(disps):
        if disp_node.inputs[0].is_linked:
            disp_out = disp_node.inputs[0].links[0].from_socket
            links.new(disp_out, mix_node.inputs[1])
        
    principled = get_principled_node(nodes)
    arrange_disp_nodes(nodes, links, disp_node, principled, output)

# Arrange displacement nodes
def arrange_disp_nodes(nodes, links, disp_node, principled, output):
    x_margine = 300.0
    disps = [d for d in nodes if 'EPBR_mix_disp' in d.name and d.type == 'MIX_RGB']
    # get the intial location
    loc = [0.0, 0.0]
    if principled:
        loc = [principled.location[0], principled.location[1] -700]
    else:
        loc = list(disp_node.location)
    # arrange the nodes
    for i, disp in enumerate(disps):
        if i > 0:
            links.new(disps[i-1].outputs[0], disp.inputs[1])
        if i == len(disps)-1:
            links.new(disp.outputs[0], disp_node.inputs[0])
        disp.location = loc
        loc[0] += x_margine
    disp_node.location = loc
    if output:
        output.location[0] = disp_node.location[0] + x_margine
        

################################################################################
############################## Properties ######################################
################################################################################

################ Easy PBR Settings #################
class Downloads(PropertyGroup):
    asset : StringProperty()
    res : StringProperty()
    file_path : StringProperty()
    alive : BoolProperty(default = True)
    stop_thread : BoolProperty(default = False)
    progress : IntProperty(
        default = 0,
        min = 0,
        max = 100,
        description = 'Progress of the download',
        subtype = 'PERCENTAGE'
    )
    
class EPBRSettings(PropertyGroup):
    name : StringProperty()
    downloads : CollectionProperty(type = Downloads)
    #    download_index : IntProperty()
    
    acg_library = {}

    shaders_previews : EnumProperty(
        name = 'PBR Shader',
        items = shaders_previews_enum,
        update = update_preview
    )
    epbr_shaders_filtering : StringProperty(
        name = 'Shaders Filter',
        default = 'AcousticFoam',
        update = update_shaders_previews,
        description = 'Live search filtering string',
        options = {'TEXTEDIT_UPDATE'}
    )
    epbr_local_res : EnumProperty(
        name = 'Available Resolutions',
        items = get_local_res_enum,
        description = 'Available Resolutions',
    )
    epbr_online_res : EnumProperty(
        name = 'Available Resolutions',
        items = get_online_res_enum,
        description = 'Available Resolutions',
    )
    epbr_categories : EnumProperty(
        name = 'Available Categories',
        items = categories_enum,
        update = update_category,
        description = 'Available Categories'        
    )
    epbr_tex_location : EnumProperty(
        items = (('LOCAL', 'Local', ''), ('ONLINE', 'Online', '')),
        name = 'Location',
        default = 'ONLINE',
        description = 'Location of the PBR Texture.\n'
            '  Local: the assets that you have already downloaded.\n'
            '  Online: available for download on AmbientCG.com.\n',
        update = update_shaders_previews
    )
    ###################### Baking Props ######################
    
    bake_dirpath : StringProperty(name="Directory Path",  
        description = "Select The folder to save the baked PBR maps in",
        subtype='DIR_PATH'
    )

    bake_color : BoolProperty(
        name = 'Color',
        default = True,
        description = 'Bake the color map'
    )
    bake_metallic : BoolProperty(
        name = 'Metallic',
        default = True,
        description = 'Bake the metallic map'
    )
    bake_roughness : BoolProperty(
        name = 'Roughness',
        default = True,
        description = 'Bake the roughness map'
    )
    bake_emission : BoolProperty(
        name = 'Emission',
        default = True,
        description = 'Bake the emission map'
    )
    bake_alpha : BoolProperty(
        name = 'Alpha',
        default = True,
        description = 'Bake the alpha map'
    )
    bake_normal : BoolProperty(
        name = 'Normal',
        default = True,
        description = 'Bake the normal map'
    )
    bake_displacement : BoolProperty(
        name = 'Displacement',
        default = True,
        description = 'Bake the displacement map'
    )
    
    bake_image_height : IntProperty(
        default = 1024,
        min = 8,
        max = 10240,
        description = 'Height of the baked images',
    )
    bake_image_width : IntProperty(
        default = 1024,
        min = 8,
        max = 10240,
        description = 'Width of the baked images',
    )
    
    bake_margin : IntProperty(
        name = 'Margin',
        default = 16,
        min = 0,
        max = 32000,
        soft_min = 0,
        soft_max = 64,
        description = 'Extends the baked result as a post process filter',
    )
    
    bake_image_format : EnumProperty(
        items = (
            ('PNG', 'PNG', ''),
            ('JPEG', 'JPEG', ''),
            ('OPEN_EXR', 'OpenEXR', ''),
            ('TIFF', 'TIFF', ''),
        ),
        name = 'Images Format',
        default = 'PNG',
        description = 'Format used for saving the baked images'
    )
        
################################################################################
############################## Preferences #####################################
################################################################################

class EPBR_Preferences(AddonPreferences):
    bl_idname = __name__
    
    preferences_tabs : EnumProperty(
        items = (
            ('LIB', 'Library', 'Library options.', 'FILE_FOLDER', 0),
            ('NODES', 'Nodes', 'Shader nodes options.', 'NODETREE', 1),
            ('KEYMAP', 'Keymap', 'List of shortcuts.', 'KEYINGSET', 2),
            ('INTERNET', 'Internet', 'Connection options.', 'URL', 3),
            ('SUPPORT', 'Suport Us', 'Show some love ^_^', 'FUND', 4),
        ),
        name = 'Preferences Tabs',
        default = 'LIB',
        description = 'Preferences Tabs'
    )
    lib_path : StringProperty(
        name="PBR Library Path",
        description = "Select The folder of the PBR library",
        subtype='DIR_PATH',
        update = update_dict
    )
    custom_node_col : BoolProperty(
        name="Use Custom Nodes Colors",
        default=True,
        description = "Use custom colors for the EPBR nodes"
    )
    shader_node_col : FloatVectorProperty(
        name = 'Shader Node Color',
        default=[0.25, 0.5, 0.75],
        size = 3,
        subtype='COLOR',
        min = 0.0,
        max = 1.0,
        description = 'Color of the shader node group'
    )
    mix_node_col : FloatVectorProperty(
        name = 'Mix Node Color',
        default=[0.75, 0.5, 0.25],
        size = 3,
        subtype='COLOR',
        min = 0.0,
        max = 1.0,
        description = 'Color of the "Mix Shaders" node'
    )
    connection_timeout : IntProperty(
        name = 'Connection timeout',
        default= 60,
        min = 5,
        max = 3600,
        description = 'In the case of failed connection with the server.\n'
            'Wait for how long for a reconnection before cancelling the download.\n'
            'Use a high value if you have a bad internet connection.\n'
            '(In Seconds)',
    )
    ignore_internet_check : BoolProperty(
        name="Ignore Internet Connection Check",
        default=False,
        description = 'The add-on checks for an internet connection before downloading.\n'
            'But the method used for checking is prone to error.\n'
            'You can disable the internet connection check by enabling this option'
            ,
    )
    def draw(self, context):
        pcoll = preview_collections["icons"]
        scn = context.scene
        wm = bpy.context.window_manager
        layout = self.layout
        col = layout.column()
        row = col.row()
        row.prop(self, 'preferences_tabs', expand = True)
        if self.preferences_tabs == 'LIB':
            box = layout.box()
            col = box.column()
            if not self.lib_path.strip():
                col.label(text = "Please select the folder of the PBR Library", icon = 'INFO')
            col.prop(self, 'lib_path')
            if self.lib_path.strip() and not confirm_lib_path(self.lib_path):
                col.alert = True
                col.label(text = "Wrong Directory.", icon = 'ERROR')
            col = box.column()
            if confirm_lib_path(self.lib_path):
                ico = pcoll["thumbs_up.png"]
                col.label(text = "Valid Library", icon_value = ico.icon_id)
                settings = scn.easy_pbr_settings
                if not len(settings):
                    ico = pcoll["library.png"]
                    col.operator("easypbr.load_json_lib", icon_value = ico.icon_id)
                else:
                    req_time = ACG_library(context).request_time()
                    if req_time is not None:
                        col.label(text = 'Last update: ' + req_time[:10], icon = 'INFO')
                    lib_download = settings[0].downloads.get('Library')
                    if not lib_download:
                        ico = pcoll["update.png"]
                        col.operator("easypbr.update_lib", icon_value = ico.icon_id)
                    else:
                        if lib_download.stop_thread:
                            col.label(text = 'Canceling...', icon = 'INFO')
                        else:
                            txt = 'Cancel downloading the library'
                            col.operator("easypbr.remove_download", icon='X', text=txt).asset = 'Library'
                if bpy.app.version >= (3, 0, 0):
                    col.operator("easypbr.add_all_as_assets", icon = 'ASSET_MANAGER')
                    
        elif self.preferences_tabs == 'NODES':
            box = layout.box()
            row = box.row()
            row.prop(self, 'custom_node_col')
            row = box.row()
            row.enabled = self.custom_node_col
            row.prop(self, 'shader_node_col')
            row = box.row()
            row.enabled = self.custom_node_col
            row.prop(self, 'mix_node_col')
        elif self.preferences_tabs == 'KEYMAP':
            # Credit to Bookyakuno for the keymap code
            # https://blenderartists.org/t/keymap-for-addons/685544/19
            box = layout.box()
            col = box.column()
            col.label(text="Keymap List:",icon="KEYINGSET")
            
            kc = wm.keyconfigs.user
            old_km_name = ""
            get_kmi_l = []
            for km_add, kmi_add in addon_keymaps:
                for km_con in kc.keymaps:
                    if km_add.name == km_con.name:
                        km = km_con
                        break

                for kmi_con in km.keymap_items:
                    if kmi_add.idname == kmi_con.idname:
                        if kmi_add.name == kmi_con.name:
                            get_kmi_l.append((km,kmi_con))

            get_kmi_l = sorted(set(get_kmi_l), key=get_kmi_l.index)

            for km, kmi in get_kmi_l:
                if not km.name == old_km_name:
                    col.label(text=str(km.name),icon="DOT")
                col.context_pointer_set("keymap", km)
                rna_keymap_ui.draw_kmi([], kc, km, kmi, col, 0)
                col.separator()
                old_km_name = km.name
        elif self.preferences_tabs == 'INTERNET':
            box = layout.box()
            row = box.row()
            row.label(text = 'Connection Timeout')
            row.prop(self, 'connection_timeout', text = '')
            row = box.row()
            row.prop(self, 'ignore_internet_check')
        elif self.preferences_tabs == 'SUPPORT':
            support_us_panel(layout)
            
    
################################################################################
################################ Operators #####################################
################################################################################

# Support us pop-up
class EPBR_OT_support_us(Operator):
    bl_idname = "easypbr.support_us"
    bl_label = "Support Us"
    bl_description = "How to support us"
    
    def execute(self, context):
        return {'FINISHED'}
    
    def draw(self, context):
        support_us_panel(self.layout)
        
    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)

############################## Templates #######################################

# Poll template for some operators (Node Utils, Baking)
class EPBR_utils_poll:
    @classmethod
    def poll(self, context):
        engines = ['BLENDER_EEVEE', 'BLENDER_WORKBENCH', 'CYCLES']
        if not context.scene.render.engine in engines:
            return False
        if not check_area(context):
            return False
        ob = context.object
        if ob is None:
            return False
        mat = ob.active_material
        if not mat:
            return False
        if not mat.use_nodes:
            return False
        return True

# Poll template for some operators (Assets)
class EPBR_assets_poll:
    @classmethod
    def poll(self, context):
        settings = context.scene.easy_pbr_settings
        if not len(settings):
            return False
        if settings[0].shaders_previews == 'EMPTY':
            return False
        return True

############################## Utilities #######################################

# Add a node group of a PBR asset
class EPBR_OT_add_pbr_shader(Operator):
    bl_idname = "easypbr.add_pbr_shader"
    bl_label = "Add PBR Shader"
    bl_description = "Add the PBR Shader as a material or a node group"
    
    method : EnumProperty(
        name = 'Method',
        items = (
            ('MAT', 'Material', ''),
            ('NG', 'Node Group', '')
        ),
        description = 'How to add the PBR Shader:\n'
            '  Node Group: Add the shader as a new node group.\n'
            '  Material: Add the shader as a new material\n',
    )
    reload : BoolProperty(
        name = 'Reload the Images',
        default = False,
        description = 'Load a new copy of images if already loaded'
    )
    
    @classmethod
    def poll(self, context):
        ob = context.object
        if ob is None:
            return False
        settings = context.scene.easy_pbr_settings
        if not len(settings):
            return False
        shader = settings[0].shaders_previews
        resolutions = get_tex_res(context, shader, 'LOCAL')
        if resolutions[0] == 'Empty':
            return False
        # get the resolutions of the downloaded asset only
        res = [i for i in resolutions if asset_downloaded(context, shader, i)]
        if not len(res):
            return False
        return True
    
    def execute(self, context):
        ob = context.object
        settings = context.scene.easy_pbr_settings[0]
        asset = settings.shaders_previews
        res = settings.epbr_local_res
        
        if not asset_downloaded(context, asset, res):
            self.report({'WARNING'}, "Empty folder.")
            return {'CANCELLED'}
        
        engines = ['BLENDER_EEVEE', 'BLENDER_WORKBENCH', 'CYCLES']
        if not context.scene.render.engine in engines:
            context.scene.render.engine = 'BLENDER_EEVEE'
        
        if self.method == 'MAT':
            add_pbr_mat(context, asset, res, self.reload)
        else:
            mat = ob.active_material
            if not mat:
                self.report({'WARNING'}, "An active material is required.")
                return {'CANCELLED'}
            else:
                add_pbr_group(context, mat, asset, res, self.reload)
            
        return {'FINISHED'}
    
    def draw(self, context):
        layout = self.layout
        scn = context.scene
        settings = context.scene.easy_pbr_settings[0]
        asset = settings.shaders_previews
        res = settings.epbr_local_res
        loc = settings.epbr_tex_location
                
        pcoll = preview_collections["shaders_previews"]
        thumb = pcoll.get(asset)
        
        box = layout.box()
        row = box.row()
        row.alignment = 'CENTER'
        row.label(text = asset_pretty_name(asset))
        if thumb:
            layout.template_icon(icon_value = thumb.icon_id, scale=9.0)
        row = layout.row()
        row.prop(self, 'method', expand = True)
        layout.prop(settings, 'epbr_local_res', text = '')
        if not asset_downloaded(context, asset, res):
            box = layout.box()
            col = box.column()
            col.alert = True
            col.label(text = 'Empty Folder!', icon = 'ERROR')
            col = box.column()
            col.label(text = 'Download the asset then try again', icon = 'INFO')
        mat = context.object.active_material
        if not mat and self.method == 'NG':
            box = layout.box()
            col = box.column()
            col.alert = True
            col.label(text = 'An active material is required.', icon = 'ERROR')
        layout.prop(self, 'reload')
        
    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)
    
# Connect the PBR node-group to the Principled node
class EPBR_OT_connect_ng_principled(EPBR_utils_poll, Operator):
    bl_idname = "easypbr.connect_ng_principled"
    bl_label = "Connect to principled node"
    bl_description = "Connect the selected PBR node-group to the selected Principled node"
    
    def execute(self, context):
        ob = context.object
        mat = ob.active_material
        nodes = mat.node_tree.nodes
        links = mat.node_tree.links
        if not len(nodes):
            self.report({'WARNING'}, "No nodes in this material.")
            return {'CANCELLED'}
        selected_nodes = [node for node in nodes if node.select]
        if not len(selected_nodes):
            m = "You have to select an Easy PBR node-group and a Pricipled node."
            self.report({'WARNING'}, m)
            return {'CANCELLED'}
        principled = None
        for node in selected_nodes:
            if node.type == 'BSDF_PRINCIPLED':
                principled = node
                break
            
        names = ['EPBR_Shader', 'EPBR_Mix_Shaders']
        pbr_ng = None
        for node in selected_nodes:
            for name in names:
                if node.type == 'GROUP' and name in node.name:
                    pbr_ng = node
                    break
            
        if not pbr_ng or not principled:
            m = "You have to select an Easy PBR node-group and a Pricipled node."
            self.report({'WARNING'}, m)
            return {'CANCELLED'}    
        
        out = get_active_output_node(nodes)
        connect_ng_principled(nodes, links, pbr_ng, principled, out)    
        
        return {'FINISHED'}
    
# Mix two PBR node-groups
class EPBR_OT_mix_pbrs(EPBR_utils_poll, Operator):
    bl_idname = "easypbr.mix_pbrs"
    bl_label = "Mix two EPBR nodes"
    bl_description = "Mix two PBR node-groups"
    
    def execute(self, context):
        ob = context.object
        mat = ob.active_material
        nodes = mat.node_tree.nodes
        links = mat.node_tree.links
        if not len(nodes):
            self.report({'WARNING'}, "No nodes in this material.")
            return {'CANCELLED'}
        selected_nodes = [node for node in nodes if node.select]
        #assets = ACG_library(context).assets()
        names = ['EPBR_Shader', 'EPBR_Mix_Shaders']
        groups = []
        for n in selected_nodes:
            for name in names:
                if name in n.name and n.type == 'GROUP':
                    groups.append(n)
                
        mix_node, ng1, ng2 = (None, None, None)
        active_node = nodes.active
        if active_node in groups and 'EPBR_Mix_Shaders' in active_node.name:
            if active_node.type == 'GROUP':
                mix_node = active_node
                groups.remove(active_node)
                
        if not mix_node:
            for n in groups:
                if 'EPBR_Mix_Shaders' in n.name and n.type == 'GROUP':
                    mix_node = n
                    groups.remove(n)
                    break
        
        
        if not len(groups):
            if mix_node:
                ng1 = mix_node
                mix_node = None
        elif len(groups) == 1:
           if not mix_node:
               ng1 = groups[0]
           else:
               ng1, ng2 = mix_slots(context, mix_node)
               if ng1 and not ng2:
                   ng2 = groups[0]
               elif ng2 and ng1:
                   ng1 = groups[0]
                   ng2 = mix_node
                   mix_node = None
               else:
                   ng1 = groups[0]
        else:
            ng1 = groups[0]
            ng2 = groups[1]
        
        mix_pbrs(context, mat, ng1, ng2, mix_node)
        
        return {'FINISHED'}
    
# Invert the links of the connected node-groups
class EPBR_OT_invert_mix_links(EPBR_utils_poll, Operator):
    bl_idname = "easypbr.invert_mix_links"
    bl_label = "Invert Mix node links"
    bl_description = "Invert the links of the Mix Shaders node"
    
    def execute(self, context):
        ob = context.object
        mat = ob.active_material
        nodes = mat.node_tree.nodes
        links = mat.node_tree.links
        if not len(nodes):
            self.report({'WARNING'}, "No nodes in this material.")
            return {'CANCELLED'}
        nodes = [i for i in nodes if i.select]
        sh = 'EPBR_Mix_Shaders'
        mix_nodes = [i for i in nodes if sh in i.name and i.type == 'GROUP']
        for mix in mix_nodes:
            invert_mix_links(context, links, mix)
        return {'FINISHED'}
    
# Change the resolution of the images inside a node-group
class EPBR_OT_change_res(EPBR_utils_poll, Operator):
    bl_idname = "easypbr.change_resolution"
    bl_label = "Change the resolution"
    bl_description = "Change the resolution of all the images inside a node-group"
    
    res : EnumProperty(
        name = 'Resolutions',
        items = get_avail_res,
        description = 'Choose a resolution from the available',
    )
    resolution : StringProperty()
    
    def execute(self, context):
        ob = context.object
        mat = ob.active_material
        nodes = mat.node_tree.nodes
        if not len(nodes):
            self.report({'WARNING'}, "No nodes in this material.")
            return {'CANCELLED'}
        active_node = nodes.active
        if not 'EPBR_Shader' in active_node.name and active_node.type == 'GROUP':
            self.report({'WARNING'}, 'You need to select a shader node-group.')
            return {'CANCELLED'}
        info = active_node.label.split()
        if not len(info) == 2:
            self.report({'WARNING'}, 'Wrong asset name.')
            return {'CANCELLED'}
        asset, resolution = info
        assets = ACG_library(context).assets()
        
        if not asset in assets:
            self.report({'WARNING'}, 'Asset "' + asset + '" not found.')
            return {'CANCELLED'}
        
        channels = asset_channels(context, asset, self.res)
        nodes = active_node.node_tree.nodes
        img_nodes = [i for i in nodes if i.type == 'TEX_IMAGE' and i.label in channels and 'EPBR_Image' in i.name]
        images = bpy.data.images
        for img in img_nodes:
            new_res = images.load(channels[img.label][1])
            img.image = new_res
        active_node.label = asset + ' ' + self.res
        
        return {'FINISHED'}
    
    def draw(self, context):
        layout = self.layout
        box = layout.box()
        if not self.resolution:
            box.alert = True
            box.label(text = 'Wrong asset name', icon = 'ERROR')
        else:
            res = 'Current resolution: ' + self.resolution
            box.label(text = res, icon = 'INFO')
            layout.prop(self, 'res')
        
    def invoke(self, context, event):
        pref = prefs(context)
        if not confirm_lib_path(pref.lib_path):
            self.report({'WARNING'}, 'Wrong Library Path')
            return {'CANCELLED'}
        asset = ''
        active_node = None
        ob = context.object
        mat = ob.active_material
        if mat.use_nodes:
            nodes = mat.node_tree.nodes
            if len(nodes):
                active_node = nodes.active
        if active_node:
            info = active_node.label.split()
            if len(info):
                asset = info[0]
        resolutions = get_tex_res(context, asset, 'LOCAL')
        self.res = resolutions[0]
        if len(info) == 2:
            self.resolution = info[1]
        else:
            self.resolution = ''
        return context.window_manager.invoke_props_dialog(self)
    
# Change the projection of the images inside a node-group
class EPBR_OT_change_projection(EPBR_utils_poll, Operator):
    bl_idname = "easypbr.change_projection"
    bl_label = "Change the projection"
    bl_description = "Change the projection method of all the images inside a node-group"
    
    projection_method : EnumProperty(
        name = 'Method',
        items = (
            ('FLAT', 'Flat', ''),
            ('BOX', 'Box', ''),
            ('SPHERE', 'Sphere', ''),
            ('TUBE', 'Tube', ''),
        ),
        description = 'Projection method',
    )
    projection_blend : FloatProperty(
        name = 'Blend',
        default = 0.0,
        min = 0.0,
        max = 1.0,
        description = 'Blend Amount'
    )
    resolution : StringProperty()
    
    def execute(self, context):
        ob = context.object
        mat = ob.active_material
        nodes = mat.node_tree.nodes
        if not len(nodes):
            self.report({'WARNING'}, "No nodes in this material.")
            return {'CANCELLED'}
        
        nodes = [i for i in nodes if i.select]
        nodes = [i for i in nodes if i.type == 'GROUP' and 'EPBR_Shader' in i.name]
        
        for n in nodes:
            sh_nodes = n.node_tree.nodes
            img_nodes = [i for i in sh_nodes if i.type == 'TEX_IMAGE' and 'EPBR_Image' in i.name]
            for img in img_nodes:
                img.projection = self.projection_method
                if self.projection_method == 'BOX':
                    img.projection_blend = self.projection_blend
        return {'FINISHED'}
    
    def draw(self, context):
        layout = self.layout
        layout.prop(self, 'projection_method')
        if self.projection_method == 'BOX':
            layout.prop(self, 'projection_blend')
        
    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)
    
# Use the node as a bump map
class EPBR_OT_use_as_bump(EPBR_utils_poll, Operator):
    bl_idname = "easypbr.use_as_bump"
    bl_label = "Use as Bump Map"
    bl_description = "Use the output of the active node as a Bump Map"
    
    outputs : EnumProperty(
        name = 'Outputs',
        items = get_node_outputs_enum,
        description = 'Choose the output to be used as a Bump Map',
    )
    len_outputs = 0
    
    def execute(self, context):
        ob = context.object
        mat = ob.active_material
        nodes = mat.node_tree.nodes
        links = mat.node_tree.links
        if not len(nodes):
            self.report({'WARNING'}, "No nodes in this material.")
            return {'CANCELLED'}
        
        active_node = nodes.active
        if active_node is None:
            self.report({'WARNING'}, "No active node in this material.")
            return {'CANCELLED'}
        
        if not self.len_outputs:
            self.report({'WARNING'}, "No valid outputs are available in the active node.")
            return {'CANCELLED'}
        
        connect_as_bump(active_node.outputs[self.outputs], nodes, links)
        return {'FINISHED'}
    
    def draw(self, context):
        layout = self.layout
        layout.prop(self, 'outputs')
        
    def invoke(self, context, event):
        outputs = get_node_outputs(context)
        self.len_outputs = len(outputs)
        if not self.len_outputs:
            return self.execute(context)
        self.outputs = outputs[0]
        if len(outputs) == 1:
            return self.execute(context)
        return context.window_manager.invoke_props_dialog(self)
    
# Use the node as a displacement map
class EPBR_OT_use_as_disp(EPBR_utils_poll, Operator):
    bl_idname = "easypbr.use_as_disp"
    bl_label = "Use as Displacement Map"
    bl_description = "Use the output of the active node as a Displacement Map"
    
    outputs : EnumProperty(
        name = 'Outputs',
        items = get_node_outputs_enum,
        description = 'Choose the output to be used as a Displacement Map',
    )
    len_outputs = 0
    
    def execute(self, context):
        ob = context.object
        mat = ob.active_material
        nodes = mat.node_tree.nodes
        links = mat.node_tree.links
        if not len(nodes):
            self.report({'WARNING'}, "No nodes in this material.")
            return {'CANCELLED'}
        
        active_node = nodes.active
        if active_node is None:
            self.report({'WARNING'}, "No active node in this material.")
            return {'CANCELLED'}
        
        if not self.len_outputs:
            self.report({'WARNING'}, "No valid outputs are available in the active node.")
            return {'CANCELLED'}
        
        connect_as_disp(active_node.outputs[self.outputs], nodes, links)
        return {'FINISHED'}
    
    def draw(self, context):
        layout = self.layout
        layout.prop(self, 'outputs')
        
    def invoke(self, context, event):
        outputs = get_node_outputs(context)
        self.len_outputs = len(outputs)
        if not self.len_outputs:
            return self.execute(context)
        self.outputs = outputs[0]
        if len(outputs) == 1:
            return self.execute(context)
        return context.window_manager.invoke_props_dialog(self)
    
############################## Assets #######################################        

# Open the web page of the asset in the web browser
class EPBR_OT_open_asset_webpage(EPBR_assets_poll, Operator):
    bl_idname = "easypbr.open_asset_webpage"
    bl_label = "Open"
    bl_description = "Open the web page of the asset in the web browser"
    
    def execute(self, context):
        settings = context.scene.easy_pbr_settings[0]
        asset = settings.shaders_previews
        url = ACG_library(context).asset_weblink(asset)
        if not url:
            self.report({'WARNING'}, "URL not found.")
            return {'CANCELLED'}
        bpy.ops.wm.url_open(url = url)
        return {'FINISHED'}

# Info about the active asset
class EPBR_OT_asset_info(EPBR_assets_poll, Operator):
    bl_idname = "easypbr.asset_info"
    bl_label = "Info"
    bl_description = "Some informations about the selected asset"
    
    def execute(self, context):
        return {'FINISHED'}
    
    def draw(self, context):
        layout = self.layout
        scn = context.scene
        settings = context.scene.easy_pbr_settings[0]
        asset = settings.shaders_previews
                        
        pcoll = preview_collections["shaders_previews"]
        thumb = pcoll.get(asset+'.png')
        
        box = layout.box()
        row = box.row()
        row.alignment = 'CENTER'
        row.label(text = asset_pretty_name(asset))
        if thumb:
            layout.template_icon(icon_value = thumb.icon_id, scale=9.0)
        box = layout.box()
        row = box.row()
        local_res = get_tex_res(context, asset, 'LOCAL')
        dwn = 'Not Downloaded yet' if local_res[0] == 'Empty' else 'Downloaded Resolutions: '
        row.label(text = dwn)
        if local_res[0] != 'Empty':
            col = box.column()
            draw_grid_items(col, local_res, 5)
        
        box = layout.box()
        row = box.row()
        online_res = get_tex_res(context, asset, 'ONLINE')
        avail = 'Empty' if online_res[0] == 'Empty' else 'Available Resolutions: '
        row.label(text = avail)
        if online_res[0] != 'Empty':
            col = box.column()
            draw_grid_items(col, online_res, 5)
            
        lib = ACG_library(context)
        box = layout.box()
        tags = lib.asset_tags(asset)
        col = box.column()
        col.label(text = 'Tags:')
        draw_grid_items(col, tags, 5)
        
        ard = lib.asset_releasedate(asset)
        box = layout.box()
        box.label(text = 'Release Date: ' + ard)
        
        acm = lib.asset_creation_method(asset)
        box = layout.box()
        box.label(text = 'Creation Method: ' + acm)
        
    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)

# Create the necessary folders and files for the PBR library
class EPBR_OT_create_dirs(Operator):
    bl_idname = "easypbr.create_dirs"
    bl_label = "Create a New Library"
    bl_description = "Create the necessary folders and files for the PBR Library"
    
    directory : StringProperty(subtype="DIR_PATH")
    
    def execute(self, context):
        if not self.directory.strip() or not os.path.exists(self.directory):
            self.report({'WARNING'}, "Invalid Path ")
            return {'CANCELLED'}
        
        folders = ['PBR_Textures', 'Previews']
        for i in folders:
            path = os.path.join(self.directory, i)
            if not os.path.exists(path):
                try:
                    os.makedirs(path)
                except Exception as error:
                    self.report({'WARNING'}, str(error))
                    return {'CANCELLED'}
        prefs(context).lib_path = self.directory
        return {'FINISHED'}
    
    def invoke(self, context, event):
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}
    
# Add the settings
class EPBR_OT_add_settings(Operator):
    bl_idname = "easypbr.add_settings"
    bl_label = "Add the Properties"
    bl_description = "Add the EPBR properties"
    
    def execute(self, context):
        enable_settings(context)
        return {'FINISHED'}
    
# Load the json library
class EPBR_OT_load_json(Operator):
    bl_idname = "easypbr.load_json_lib"
    bl_label = "Load the library"
    bl_description = "Load the database of the library into the blend file"
    
    def execute(self, context):
        enable_settings(context)
        coll = context.scene.easy_pbr_settings[0]
        lib = coll.acg_library
        if len(lib):
            return {'FINISHED'}
        
        lib_path = prefs(context).lib_path
        json_file = os.path.join(lib_path, "AmbientCG_lib.json")
        
        lib_dict = load_json_lib(json_file)
        if lib_dict:
            for key in lib_dict:
                lib[key] = lib_dict[key]
            filter = coll.epbr_shaders_filtering
            category = coll.epbr_categories
            if not filter.strip():
                coll.epbr_shaders_filtering = category
        else:
            msg = ("Can't load the library!\n"
                "Reinstalling the addon could solve this problem.")
            self.report({'WARNING'}, msg)
        return {'FINISHED'}
    
# Add all the downloaded assets to EasyPBR library
class EPBR_OT_mark_all(Operator):
    bl_idname = "easypbr.mark_all_as_assets"
    bl_label = "Mark all as assets"
    bl_description = ("Load all the downloaded assets, then mark them as assets.\n"
    "To be used in the Asset Browser.\n"
    "For Blender 3.0 and above")
    
    def execute(self, context):
        if bpy.app.version < (3, 0, 0):
            self.report({'WARNING'}, "This operator is for Blender 3.0 and above.")
            return {'CANCELLED'}
        
        lib_path = prefs(context).lib_path
        if not confirm_lib_path(lib_path):
            self.report({'WARNING'}, "Wrong Library Path.")
            return {'CANCELLED'}
            
        # Make sure the EPBR Collection is there
        enable_settings(context)
        coll = context.scene.easy_pbr_settings[0]
        
        # A trick to reload the library
        prefs(context).lib_path = lib_path
        
        lib = coll.acg_library
        if not len(lib):
            self.report({'WARNING'}, "No Asset Found!")
            return {'CANCELLED'}
        mark_all_as_assets(context)
        return {'FINISHED'}
    
# Add all the downloaded assets to EasyPBR library (background process)
class EPBR_OT_add_all_as_assets(Operator):
    bl_idname = "easypbr.add_all_as_assets"
    bl_label = "Add All available assets to the Library"
    bl_description = ("Add all the downloaded assets to EasyPBR library.\n"
    "To be used in the Asset Browser.\n"
    "For Blender 3.0 and above")
    
    reload_all_assets : BoolProperty(
        name = 'Reload all the assets',
        default = False,
        description = 'Clear then reload all the downloaded assets'
        )
    
    def execute(self, context):
        if bpy.app.version < (3, 0, 0):
            self.report({'WARNING'}, "This operator is for Blender 3.0 and above.")
            return {'CANCELLED'}
        
        lib_path = prefs(context).lib_path
        if not confirm_lib_path(lib_path):
            self.report({'WARNING'}, "Wrong Library Path.")
            return {'CANCELLED'}
        
        blend_file = os.path.join(lib_path, "Assets_Library.blend")
        if not os.path.exists(blend_file):
            msg = 'The blend file for the library is missing.'
            self.report({'WARNING'}, msg)
            return {'CANCELLED'}
            
        add_all_as_assets(blend_file, self.reload_all_assets)
        return {'FINISHED'}
    
    def draw(self, context):
        layout = self.layout
        box = layout.box()
        col = box.column(align = True)
        col.label(text = 'This operation will take few seconds.', icon = 'INFO')
        col.label(text = 'Depending on the number of downloaded assets.', icon = 'BLANK1')
        layout.prop(self, 'reload_all_assets')
        
    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)
    

############################## Downloads #######################################
    
# Stop/Romove Download
class EPBR_OT_remove_download(Operator):
    bl_idname = "easypbr.remove_download"
    bl_label = "Cancel"
    bl_description = "Remove/Cancel this download"
    
    asset : StringProperty()
    
    def execute(self, context):
        settings = context.scene.easy_pbr_settings[0]
        downloads = settings.downloads
        prop = downloads.get(self.asset)
        if prop is not None:
            prop.stop_thread = True
        thread = get_asset_thread(self.asset)
        if thread is not None:
            thread.stop = True
        return {'FINISHED'}
            
# Download a PBR Shader    
class EPBR_OT_download_shader(EPBR_assets_poll, Operator):
    bl_idname = "easypbr.download_shader"
    bl_label = "Download This Shader"
    bl_description = "Download the selected shader"
    
    def execute(self, context):
        settings = context.scene.easy_pbr_settings[0]
        # if something is already downloading we will assume that there
        # is/was an internet connection, to minimize the check for internet
        if not len(settings.downloads):
            ignore_check = prefs(context).ignore_internet_check
            if not ignore_check:
                if not check_internet():
                    self.report({'WARNING'}, "No Internet Connection.")
                    return {'CANCELLED'}
        
        asset = settings.shaders_previews
        res = settings.epbr_online_res
        
        if (asset + res) in settings.downloads:
            self.report({'INFO'}, "This file is already downloading.")
            return {'CANCELLED'}
        lib = ACG_library(context)
        link = lib.asset_link(asset, res)
        
        if not link:
            self.report({'WARNING'}, "Download Link not available.")
            return {'CANCELLED'}
        
        filetype = lib.asset_filetype(asset, res)
        if not filetype.lower() == 'zip':
            self.report({'WARNING'}, "Unexpected file format.")
            return {'CANCELLED'}
        
        pbr_tex_path = ACG_paths(context).pbr_tex_path()
        asset_dir = os.path.join(pbr_tex_path, asset, res)
        if not os.path.exists(asset_dir):
            os.makedirs(asset_dir)
        filepath = os.path.join(asset_dir, asset + '.zip')
        
        # the property for the progress bar
        down = settings.downloads.add()
        down.asset = asset
        down.res = res
        down.name = asset + res
        down.file_path = filepath
        
        timeout = prefs(context).connection_timeout
        # the download thread
        args = (asset, res, link, filepath, timeout)
        thread = threading.Thread(target=download_asset, args=args)
        thread.name = asset + res
        thread.progress = 0.0
        thread.stop = False
        thread.start()
        
        global download_threads
        download_threads.append(thread)
        return {'FINISHED'}
    
    def draw(self, context):
        layout = self.layout
        scn = context.scene
        settings = context.scene.easy_pbr_settings[0]
        asset = settings.shaders_previews
        res = settings.epbr_online_res
        loc = settings.epbr_tex_location
                
        pcoll = preview_collections["shaders_previews"]
        thumb = pcoll.get(asset)
        
        box = layout.box()
        row = box.row()
        row.alignment = 'CENTER'
        row.label(text = asset_pretty_name(asset))
            
        if thumb:
            layout.template_icon(icon_value = thumb.icon_id, scale=9.0)    
        layout.prop(settings, 'epbr_online_res', text = '')
        size = ACG_library(context).asset_size(asset, res)
        box = layout.box()
        mb_size = str(round(int(size)/1000000, 2))
        box.label(text = 'Size: ' + mb_size + ' MB')
        
        if asset_downloaded(context, asset, res):
            box = layout.box()
            box.label(text = 'Already Downloaded', icon = 'CHECKMARK')
            col = box.column()
            col.alert = True
            col.label(text = 'Overwrite?', icon = 'QUESTION')
        
    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)
    
# Redownload a PBR Shader    
class EPBR_OT_redownload_shader(EPBR_assets_poll, Operator):
    bl_idname = "easypbr.redownload_shader"
    bl_label = "Download again"
    bl_description = "Download again"
    
    asset : StringProperty()
    
    def execute(self, context):
        ignore_check = prefs(context).ignore_internet_check
        if not ignore_check:
            if not check_internet():
                self.report({'WARNING'}, "No Internet Connection.")
                return {'CANCELLED'}
        
        settings = context.scene.easy_pbr_settings[0]
        down = settings.downloads.get(self.asset)
        asset = down.asset
        res = down.res
        lib = ACG_library(context)
        
        link = lib.asset_link(asset, res)
        if not link:
            self.report({'WARNING'}, "Download Link not available.")
            return {'CANCELLED'}
        
        filetype = lib.asset_filetype(asset, res)
        if not filetype.lower() == 'zip':
            self.report({'WARNING'}, "Unexpected file format.")
            return {'CANCELLED'}
        
        pbr_tex_path = ACG_paths(context).pbr_tex_path()
        asset_dir = os.path.join(pbr_tex_path, asset, res)
        if not os.path.exists(asset_dir):
            os.makedirs(asset_dir)
        filepath = os.path.join(asset_dir, asset + '.zip')
        down.file_path = filepath
        
        timeout = prefs(context).connection_timeout
        global download_threads
            
        old_thread = get_asset_thread(self.asset)
        if old_thread is not None:
            download_threads.remove(old_thread)
        
        args = (asset, res, link, filepath, timeout)
        thread = threading.Thread(target=download_asset, args=args)
        thread.name = self.asset
        thread.progress = 0.0
        thread.stop = False
        thread.start()
        
        down.alive = True
        
        download_threads.append(thread)
        return {'FINISHED'}
        
# Download the missing previews
class EPBR_OT_download_previews(Operator):
    bl_idname = "easypbr.download_previews"
    bl_label = "Download the previews"
    bl_description = "Download the missing previews for the available assets"

    def execute(self, context):
        ignore_check = prefs(context).ignore_internet_check
        if not ignore_check:
            if not check_internet():
                self.report({'WARNING'}, "No Internet Connection.")
                return {'CANCELLED'}
        
        settings = context.scene.easy_pbr_settings[0]
        if 'Previews' in settings.downloads:
            self.report({'INFO'}, "The Previews are already downloading.")
            return {'CANCELLED'}
        
        lib = ACG_library(context)
        assets = lib.assets()
        total = len(assets)
        available = available_previews(context)
        assets = [i for i in assets if i+'.png' not in available]
        links = [lib.preview_link(i, '256-PNG') for i in assets]
        
        prevs_path = ACG_paths(context).previews_path()
        
        down = settings.downloads.add()
        down.name = 'Previews'
        down.asset = 'Previews'
        
        timeout = prefs(context).connection_timeout
        args = (assets, links, total, prevs_path, timeout)
        thread = threading.Thread(target=download_previews, args=args)
        thread.name = 'Previews'
        thread.progress = 0.0
        thread.stop = False
        thread.start()
        
        global download_threads
        download_threads.append(thread)
        
        return {'FINISHED'}
    
# Download the library json file then update the library
class EPBR_OT_update_lib(Operator):
    bl_idname = "easypbr.update_lib"
    bl_label = "Update AmbientCG Library"
    bl_description = "Update the local database by downloading the library from AmbientCG.com"
    
    @classmethod
    def poll(self, context):
        settings = context.scene.easy_pbr_settings
        if not len(settings):
            return False
        return True

    def execute(self, context):
        ignore_check = prefs(context).ignore_internet_check
        if not ignore_check:
            if not check_internet():
                self.report({'WARNING'}, "No Internet Connection.")
                return {'CANCELLED'}
        
        settings = context.scene.easy_pbr_settings[0]
        if 'Library' in settings.downloads:
            self.report({'INFO'}, "The library is already downloading.")
            return {'CANCELLED'}
        
        len_assets = 0
        lib = settings.acg_library
        if lib:
            len_assets = len(lib['Assets'])
        assets_number = get_assets_number()
        if assets_number <= len_assets:
            self.report({'INFO'}, "Your library is up to date.")
            return {'CANCELLED'}
        
        down = settings.downloads.add()
        down.name = 'Library'
        down.asset = 'Library'
        
        timeout = prefs(context).connection_timeout
        paths = ACG_paths(context)
        file_path = paths.lib_json_path()
        lib_path = paths.lib_path()
        backup_file_path = os.path.join(lib_path, 'backup.json')
        args = (timeout, file_path, backup_file_path, assets_number)
        
        thread = threading.Thread(target=update_lib, args=args)
        thread.name = 'Library'
        thread.progress = 0.0
        thread.stop = False
        thread.start()
        
        global download_threads
        download_threads.append(thread)
        
        return {'FINISHED'}
    
############################## Baking #######################################
def image_ext(format):
    formats = {
        'PNG': '.png',
        'JPEG': '.jpg',
        'OPEN_EXR': '.exr',
        'TIFF': '.tif',
    }
    return formats[format]

def maps_to_bake(settings):
    maps = {
        'Color': 'bake_color',
        'Alpha': 'bake_alpha',
        'Emission': 'bake_emission',
        'Roughness': 'bake_roughness',
        'Displacement': 'bake_displacement',
        'Normal': 'bake_normal',
        'Metallic': 'bake_metallic',
    }
    return [i for i in maps if getattr(settings, maps[i])]

def displacement_socket(output):
    if not output.inputs[2].is_linked:
        return None
    disp_node = output.inputs[2].links[0].from_node
    if not disp_node.type == 'DISPLACEMENT':
        return None
    if disp_node.inputs[0].is_linked:
        return disp_node.inputs[0].links[0].from_socket
    return None

# Bake the BPR shader
class EPBR_OT_bake_pbr_maps(EPBR_utils_poll, Operator):
    bl_idname = "easypbr.bake_pbr_maps"
    bl_label = "Bake"
    bl_description = "Bake the selected PBR Maps"

    _timer = None
    nodes = None
    links = None
    principled = None
    sockets = {}
    current_image = None
    render_engine = None
    dir = ''
    margin = 16
    bake_again = False    
    
    def bake_map(self):
        current_map = baking_queue[0]
        image_node = self.nodes.get('EPBR_Image_Bake')
        if not image_node:
            image_node = self.nodes.new(type = 'ShaderNodeTexImage')
            image_node.name = 'EPBR_Image_Bake'
        image_node.image = self.current_image
        colorspace = 'sRGB' if current_map in ['Color', 'Emission'] else 'Non-Color'
        image_node.image.colorspace_settings.name = colorspace
        self.links.new(self.sockets[current_map], self.output.inputs[0])
        self.nodes.active = image_node
        channel = 'NORMAL' if current_map == 'Normal' else 'EMIT'
        ret = bpy.ops.object.bake('INVOKE_DEFAULT', type = channel, margin = self.margin)
        # a workaround to test if the previous baking operation finished, coupled with "image.is_dirty"
        # since it's not possible to track the execution of the baking operator AFAIK
        # The operator will return {'CANCELLED'} if another instance is running
        self.bake_again = ret == {'CANCELLED'}        
        
    def new_image(self, settings):
        current_map = baking_queue[0]
        ext = image_ext(settings.bake_image_format)
        filepath = os.path.join(self.dir, current_map + ext)
        images = bpy.data.images
        width = settings.bake_image_width
        height = settings.bake_image_height
        image = images.new(current_map, width, height)
        #image.file_format = settings.bake_image_format
        image.filepath_raw = filepath
        return image

    def modal(self, context, event):
        # cancel on Escap key press    
        if event.type in {'ESC',}:
            self.cancel(context)
            return {'CANCELLED'}
        
        if event.type == 'TIMER':
            # check if the baking finished
            if not self.current_image.is_dirty:
                if self.bake_again:
                    self.bake_map()
                return {'PASS_THROUGH'}
            
            global baking_queue
            current_map = baking_queue[0]
            settings = context.scene.easy_pbr_settings[0]
            # save the baked image to the selected folder
            self.current_image.file_format = settings.bake_image_format
            self.current_image.save()
            # remove the baked image from the internal data
            bpy.data.images.remove(self.current_image)
            # remove from the queue
            baking_queue.remove(current_map)
            # if the queue is empty then exit
            if not len(baking_queue):
                self.cancel(context)
                self.report({'INFO'}, 'Baking Finished!')
                return {'FINISHED'}
            # Next Map
            self.current_image = self.new_image(settings)
            self.bake_map()
        return {'PASS_THROUGH'}

    def execute(self, context):
        global baking_queue
        if len(baking_queue):
            self.report({'WARNING'}, "Another baking instance is running")
            return {'CANCELLED'}
        
        ob = context.object
        mat = ob.active_material
        self.nodes = mat.node_tree.nodes
        self.links = mat.node_tree.links
        self.sockets = {} # reset
        
        if not len(self.nodes):
            self.report({'WARNING'}, "No nodes in this material.")
            return {'CANCELLED'}
        
        self.principled = self.nodes.active
        if not self.principled or not self.principled.type == 'BSDF_PRINCIPLED':
            self.report({'WARNING'}, 'The active node must be a Principled node.')
            return {'CANCELLED'}
        
        self.output = get_active_output_node(self.nodes)
        if not self.output:
            self.report({'WARNING'}, 'An Output node is required.')
            return {'CANCELLED'}
        
        settings = context.scene.easy_pbr_settings[0]
        self.dir = settings.bake_dirpath
        if not self.dir.strip() or not os.path.exists(self.dir):
            self.report({'WARNING'}, 'Wrong Directory Path.')
            return {'CANCELLED'}
            
        disp_socket = displacement_socket(self.output)
        if disp_socket:
            self.sockets['Displacement'] = disp_socket
        
        self.render_engine = context.scene.render.engine
        if not self.render_engine == 'CYCLES':
            context.scene.render.engine = 'CYCLES'
        
        idx = principled_indexs()
        for k in idx.keys():
            socket = None
            i = idx[k]
            if k == 'Normal':
                socket = self.principled.outputs[0]
            elif self.principled.inputs[i].is_linked:
                socket = self.principled.inputs[i].links[0].from_socket
            if socket:
                self.sockets[k] = socket
        
        maps_bake = maps_to_bake(settings)
        baking_queue = [i for i in list(self.sockets) if i in maps_bake]
        if not len(baking_queue):
            self.report({'WARNING'}, 'No map to bake.')
            return {'CANCELLED'}
        
        self.current_image = self.new_image(settings)
        # to keep track of the operator
        global baking_op
        baking_op = self
        # start baking the first map
        self.bake_map()
        
        # cancel if the baking operator is already running
        if self.bake_again:
            self.cancel(context)
            self.report({'WARNING'}, "Another baking instance is running")
            return {'CANCELLED'}
        # modal timer, 5 times a second seems to be fine
        wm = context.window_manager
        self._timer = wm.event_timer_add(0.2, window=context.window)
        wm.modal_handler_add(self)
        return {'RUNNING_MODAL'}

    def cancel(self, context):
        # remove the timer
        if self._timer is not None:
            wm = context.window_manager
            wm.event_timer_remove(self._timer)
        # clear the baking queue and reset baking_op
        global baking_queue
        baking_queue = []
        global baking_op
        baking_op = None
        # restore the render engine
        context.scene.render.engine = self.render_engine
        # delete the image node used for baking
        image_node = self.nodes.get('EPBR_Image_Bake')
        if image_node:
            self.nodes.remove(image_node)
        # reconnect the pricipled output
        self.links.new(self.principled.outputs[0], self.output.inputs[0])
        
# Clear the baking queue
class EPBR_OT_clear_baking_queue(Operator):
    bl_idname = "easypbr.clear_baking_queue"
    bl_label = "Clear"
    bl_description = "Clear the baking queue"
    
    def execute(self, context):
        global baking_queue
        baking_queue = []
        
        global baking_op
        baking_op = None
        return {'FINISHED'}

################################################################################
##################################### UI #######################################
################################################################################

# Display a list of items in a grid
def draw_grid_items(layout, items, cols):
    num = len(items)
    if cols >= num:
        rows = 1
    else:
        rows = num // cols
        rows = rows+1 if num%cols else rows
    for i in range(rows):
        layout.label(text = ', '.join(items[:cols]))
        items = items[cols:]
    
# Template Panel        
class EPBRPanel:
    bl_space_type = "NODE_EDITOR"
    bl_region_type = "UI"
    bl_category = "EPBR"
    
    @classmethod
    def poll(self, context):
        engines = ['BLENDER_EEVEE', 'BLENDER_WORKBENCH', 'CYCLES']
        if not context.scene.render.engine in engines:
            return False
        if not check_area(context):
            return False
        pref = prefs(context)
        if not confirm_lib_path(pref.lib_path):
            return False       
        scn = context.scene
        settings = scn.easy_pbr_settings
        if not len(settings) or not settings[0].acg_library:
            return False
        return True
    
# Support us panel
def support_us_panel(layout):
    pcoll = preview_collections["icons"]
    box = layout.box()
    ico = pcoll["coa.png"]
    box.label(text = 'Support the add-on development:', icon_value=ico.icon_id)
    
    ico = pcoll["gumroad_logo.png"]
    url = 'https://codeofart.gumroad.com/'
    text = 'Our store in Gumroad'
    box.operator("wm.url_open", text = text, icon_value=ico.icon_id).url = url
    
    ico = pcoll["blender_market_logo.png"]
    url = 'https://blendermarket.com/creators/monaime'
    text = 'Our store in the Blender Market'
    box.operator("wm.url_open", text = text, icon_value=ico.icon_id).url = url
    
    ico = pcoll["ambientcg_logo.png"]
    box.label(text = 'Support the PBR library (AmbientCG.com):', icon_value=ico.icon_id)
    
    ico = pcoll["patreon_logo.png"]
    url = 'https://patreon.com/ambientcg'
    text = 'Become a Patreon'
    box.operator("wm.url_open", text = text, icon_value=ico.icon_id).url = url
    
    ico = pcoll["ko-fi.png"]
    url = 'https://ko-fi.com/ambientcg'
    text = 'Donate to AmbientCG'
    box.operator("wm.url_open", text = text, icon_value=ico.icon_id).url = url

# Assets Panel
class EPBR_PT_assets(EPBRPanel, Panel):
    bl_label = "Assets"
    
    @classmethod
    def poll(self, context):
        engines = ['BLENDER_EEVEE', 'BLENDER_WORKBENCH', 'CYCLES']
        if not context.scene.render.engine in engines:
            return False
        if not check_area(context):
            return False
        return True
    
    def draw_header(self, context):
        layout = self.layout
        row = layout.row(align = True)
        layout.alignment = 'RIGHT'
        pcoll = preview_collections["icons"]
        row.operator("easypbr.support_us", text = "", emboss = False, icon = 'FUND')
        
        ico = pcoll["ambientcg_logo.png"]
        url = 'https://ambientcg.com/'
        row.operator("wm.url_open", text = '', emboss = False, icon_value=ico.icon_id).url = url
        
        row.separator()
    
    def draw(self, context):
        scn = context.scene
        layout = self.layout
        col = layout.column()
        preferences = prefs(context)
        settings = scn.easy_pbr_settings
        pcoll = preview_collections["icons"]
        if preferences is None:
            layout.label(text = "Can't read the Preferences!", icon = 'Error')
            return
        lib_path = preferences.lib_path
        if not lib_path.strip():
            col.prop(preferences, 'lib_path', text = '')
            col.label(text = "Select the Library folder", icon = 'INFO')
            return
            
        if not confirm_lib_path(lib_path):
            col.prop(preferences, 'lib_path', text = '')
            col.alert = True
            col.label(text = 'Wrong Directory.', icon = 'ERROR')
            return
        
        if not len(settings) or not settings[0].acg_library:
            ico = pcoll['library.png']
            col.scale_y = 1.3
            col.operator("easypbr.load_json_lib", icon_value = ico.icon_id)
            return
        
        assets = ACG_library(context).assets()
        len_assets = len(assets) if assets else 0
        avail_prevs = available_previews(context)
        coll = settings[0]
        filter = coll.epbr_shaders_filtering
        loc = coll.epbr_tex_location
        
        results = assets_list(context, filter, loc)
        len_results = len(results)
        if len_results == 1:
            if results[0] == 'EMPTY':
                len_results = 0
        
        previews = coll.downloads.get('Previews')
        if previews:
            #col.prop(previews, 'alive')
            row = col.row()
            if not previews.alive:
                row.alert = True
                row.label(text = 'Download Failed', icon = 'ERROR')
            else:
                row.label(text = 'Downloading the previews...')
            col.enabled = not previews.stop_thread
            row = col.row(align = True)
            row.scale_y = 0.75
            row.prop(previews, 'progress', slider = True, text = str(len(avail_prevs))+'/'+str(len_assets))
            row.operator("easypbr.remove_download", icon='X', text="").asset = 'Previews'
        elif len(avail_prevs) < len_assets and len_assets:
            col = layout.column()
            col.label(text = str(len(assets)-len(avail_prevs)) + ' Missing Previews', icon = 'INFO')
            col.operator("easypbr.download_previews", icon = 'IMPORT')
        col = layout.column(align = True)
        row = col.row()
        row.prop(coll, 'epbr_tex_location', expand = True)
        col.prop(coll, 'epbr_categories', text = '')
        col.prop(coll, 'epbr_shaders_filtering', text = '', icon = 'VIEWZOOM')
        col.label(text = str(len_results) + ' Results', icon = 'INFO')
        col.template_icon_view(coll, "shaders_previews", show_labels=True,scale = 7, scale_popup = 5)
        box = col.box()
        row = box.row()
        row.alignment = 'CENTER'
        row.label(text = asset_pretty_name(coll.shaders_previews))
        #box = col.box()
        row = box.row()
        row.scale_y, row.scale_x = (1.25, 1.25)
        row.alignment = 'CENTER'
        row.operator("easypbr.download_shader", text = '', icon = 'IMPORT')
        row.operator("easypbr.add_pbr_shader", text = '', icon = 'ADD')
        row.operator("easypbr.open_asset_webpage", text = '', icon = 'URL')
        row.operator("easypbr.asset_info", text = '', icon = 'INFO')
        row = box.row()
#        col.separator()
#        box = col.box()
#        row = box.row()
#        resolutions = get_tex_res(context, coll.shaders_previews, 'LOCAL')
#        dwn = 'Not Downloaded yet' if resolutions[0] == 'Empty' else 'Downloaded Resolutions: '
#        row.label(text = dwn, icon = 'INFO')
#        if resolutions[0] != 'Empty':
#            col = box.column()
#            draw_grid_items(col, resolutions, 3)
        
# Utils Panel
class EPBR_PT_nodes_Utilities(EPBRPanel, Panel):
    bl_label = "Nodes Utilities"
    bl_options = {"DEFAULT_CLOSED"}
    
    @classmethod
    def poll(self, context):
        engines = ['BLENDER_EEVEE', 'BLENDER_WORKBENCH', 'CYCLES']
        if not context.scene.render.engine in engines:
            return False
        if not check_area(context):
            return False
        return True
    
    def draw(self, context):
        pcoll = preview_collections["icons"]
        layout = self.layout
        col = layout.column()
        
        ico = pcoll["connect_principled.png"]
        col.operator("easypbr.connect_ng_principled", icon_value = ico.icon_id)
        
        ico = pcoll["mix_epbrs.png"]        
        col.operator("easypbr.mix_pbrs", icon_value = ico.icon_id)
        
        ico = pcoll["invert_mix.png"]
        col.operator("easypbr.invert_mix_links", icon_value = ico.icon_id)
        
        ico = pcoll["change_res.png"]
        col.operator("easypbr.change_resolution", icon_value = ico.icon_id)
        
        ico = pcoll["change_projection.png"]
        col.operator("easypbr.change_projection", icon_value = ico.icon_id)
        
        ico = pcoll["use_bump.png"]
        col.operator("easypbr.use_as_bump", icon_value = ico.icon_id)
        
        ico = pcoll["use_disp.png"]
        col.operator("easypbr.use_as_disp", icon_value = ico.icon_id)
        
# Baking Panel
class EPBR_PT_bake(EPBRPanel, Panel):
    bl_label = "Bake PBR Maps"
    bl_options = {"DEFAULT_CLOSED"}
    
    @classmethod
    def poll(self, context):
        engines = ['BLENDER_EEVEE', 'BLENDER_WORKBENCH', 'CYCLES']
        if not context.scene.render.engine in engines:
            return False
        if not check_area(context):
            return False
        return True
    
    def draw(self, context):
        layout = self.layout
        pcoll = preview_collections["icons"]
        
        if len(baking_queue):
            try:
                # test if the baking operator is alive
                x = baking_op.bl_label
            except:
                col = layout.column()
                col.alert = True
                col.label(text = "An error occured while baking", icon = 'ERROR')
                col.operator('easypbr.clear_baking_queue', icon = 'X')
            else:
                box = layout.box()
                row = box.row()
                row.alignment = 'CENTER'
                row.label(text = 'BAKING...')
                ico = pcoll['baking.png']
                layout.template_icon(icon_value = ico.icon_id, scale=6.0)
                box = layout.box()
                box.label(text = 'Press Escap to cancel', icon = 'INFO')
                box = layout.box()
                box.alert = True
                box.label(text = "Don't modify the nodes", icon = 'INFO')
            finally:
                box = layout.box()
                box.label(text = 'Maps left:', icon = 'INFO')
                draw_grid_items(box, baking_queue, 3)
            return
        
        scn = context.scene
        col = layout.column()
        if not len(scn.easy_pbr_settings):
            col.scale_y = 1.3
            col.operator("easypbr.add_settings", icon = 'ADD')
            return
            
        settings = scn.easy_pbr_settings[0]
        col.prop(settings, 'bake_dirpath', text = '')
        
        dirpath = settings.bake_dirpath
        if not settings.bake_dirpath.strip():
            col.alert = True
            col.label(text = 'Select the output folder', icon = 'INFO')
        elif not os.path.exists(settings.bake_dirpath):
            col.alert = True
            col.label(text = 'Wrong Directory Path', icon = 'ERROR')
            
        col = layout.column(align = True)
        col.prop(settings, 'bake_color', text = 'Color', icon = 'BLANK1')
        col.prop(settings, 'bake_metallic', text = 'Metallic', icon = 'BLANK1')
        col.prop(settings, 'bake_roughness', text = 'Roughness', icon = 'BLANK1')
        col.prop(settings, 'bake_emission', text = 'Emission', icon = 'BLANK1')
        col.prop(settings, 'bake_alpha', text = 'Alpha', icon = 'BLANK1')
        col.prop(settings, 'bake_normal', text = 'Normal', icon = 'BLANK1')
        col.prop(settings, 'bake_displacement', text = 'Displacement', icon = 'BLANK1')
        
        col.separator()
        col.prop(settings, 'bake_image_height', text = 'Images Height')
        col.prop(settings, 'bake_image_width', text = 'Images Width')
        
        col.separator()
        col.prop(settings, 'bake_margin', text = 'Margin')
        
        col.separator()
        col.prop(settings, 'bake_image_format', text = 'Format', icon = 'FILE_IMAGE')
        
        col = layout.column()
        col.scale_y = 1.5
        col.operator('easypbr.bake_pbr_maps', icon = 'IMAGE')
        
        
# Downloads Panel
class EPBR_PT_downloads(EPBRPanel, Panel):
    bl_label = "Downloads"
    
    def draw(self, context):
        layout = self.layout
        scn = context.scene
        settings = scn.easy_pbr_settings[0]
        downloads = settings.downloads
        
        if not len(downloads):
            box = layout.box()
            box.label(text = 'No Downloads', icon = 'INFO')
            return
        
        for dwn in downloads:
            box = layout.box()
            if not dwn.alive:
                row = box.row()
                row.alert = True
                row.label(text = 'Download Failed', icon = 'ERROR')
            row = box.row(align = True)
            row.scale_y = 0.75
            row.enabled = not dwn.stop_thread
            text = dwn.asset + ' | ' + dwn.res if dwn.res else dwn.asset
            row.prop(dwn, 'progress', slider = True, text = text)
            if not dwn.alive and dwn.name not in ['Library', 'Previews']:
                row.operator("easypbr.redownload_shader", icon='FILE_REFRESH', text="").asset = dwn.name
            row.operator("easypbr.remove_download", icon='X', text="").asset = dwn.name
                
################################################################################
################################ Register ######################################
################################################################################

classes = (
    EPBR_PT_assets,
    EPBR_PT_nodes_Utilities,
    EPBR_PT_bake,
    EPBR_PT_downloads,
    EPBR_Preferences,
    EPBR_OT_support_us,
    EPBR_OT_add_pbr_shader,
    EPBR_OT_connect_ng_principled,
    EPBR_OT_mix_pbrs,
    EPBR_OT_invert_mix_links,
    EPBR_OT_change_res,
    EPBR_OT_change_projection,
    EPBR_OT_use_as_bump,
    EPBR_OT_use_as_disp,
    EPBR_OT_open_asset_webpage,
    EPBR_OT_asset_info,
    EPBR_OT_create_dirs,
    EPBR_OT_add_settings,
    EPBR_OT_load_json,
    EPBR_OT_mark_all,
    EPBR_OT_add_all_as_assets,
    EPBR_OT_remove_download,
    EPBR_OT_download_shader,
    EPBR_OT_redownload_shader,
    EPBR_OT_download_previews,
    EPBR_OT_update_lib,
    EPBR_OT_bake_pbr_maps,
    EPBR_OT_clear_baking_queue,
    Downloads,
    EPBRSettings,
)

def register():
    from bpy.utils import register_class
    for cls in classes:
        register_class(cls)
    
    bpy.types.Scene.easy_pbr_settings = CollectionProperty(type = EPBRSettings)
    
    # Previews for the assets
    p_coll = bpy.utils.previews.new()
    p_coll.shaders_previews = ()
    p_coll.refresh = ""
    preview_collections["shaders_previews"] = p_coll
    # The Icons
    pcoll = bpy.utils.previews.new()
    icons_dir = os.path.join(addon_folder, "Images")
    for i in os.listdir(icons_dir):
        if not i.lower().endswith('.png'):
            continue
        pcoll.load(i, os.path.join(icons_dir, i), 'IMAGE')
    preview_collections["icons"] = pcoll
    
    # Keymaps
    wm = bpy.context.window_manager
    kc = wm.keyconfigs.addon
    if kc:
        km = wm.keyconfigs.addon.keymaps.new(name='Node Editor', space_type="NODE_EDITOR")
        # Connect
        op = EPBR_OT_connect_ng_principled.bl_idname
        kmi = km.keymap_items.new(op, type='P', value='PRESS', alt=True)
        addon_keymaps.append((km, kmi))
        # Mix
        op = EPBR_OT_mix_pbrs.bl_idname
        kmi = km.keymap_items.new(op, type='M', value='PRESS', alt=True)
        addon_keymaps.append((km, kmi))
        # Invert
        op = EPBR_OT_invert_mix_links.bl_idname
        kmi = km.keymap_items.new(op, type='I', value='PRESS', alt=True)
        addon_keymaps.append((km, kmi))
        # Change resolution
        op = EPBR_OT_change_res.bl_idname
        kmi = km.keymap_items.new(op, type='C', value='PRESS', alt=True)
        addon_keymaps.append((km, kmi))
        # Change blending
        op = EPBR_OT_change_projection.bl_idname
        kmi = km.keymap_items.new(op, type='U', value='PRESS', alt=True)
        addon_keymaps.append((km, kmi))
        # Use as bump
        op = EPBR_OT_use_as_bump.bl_idname
        kmi = km.keymap_items.new(op, type='B', value='PRESS', alt=True)
        addon_keymaps.append((km, kmi))
        # Use as displacement
        op = EPBR_OT_use_as_disp.bl_idname
        kmi = km.keymap_items.new(op, type='V', value='PRESS', alt=True)
        addon_keymaps.append((km, kmi))
        
    # Timer for monitoring the downloads
    bpy.app.timers.register(monitor_downloads, first_interval=1, persistent=True)    
    
def unregister():
    from bpy.utils import unregister_class
    for cls in reversed(classes):
        unregister_class(cls)
    
    del bpy.types.Scene.easy_pbr_settings
    
    for pcoll in preview_collections.values():
        bpy.utils.previews.remove(pcoll)
    preview_collections.clear()
    
    # Clear the keymaps
    for km, kmi in addon_keymaps:
        km.keymap_items.remove(kmi)
    addon_keymaps.clear()
    # Unregister the downloads timer
    if bpy.app.timers.is_registered(monitor_downloads):
        bpy.app.timers.unregister(monitor_downloads)
        
#if __name__ == "__main__":
#    register()