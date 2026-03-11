import bpy
from RBX_Toolbox import glob_vars

rbx_anim_error = None
unhide_store = []



######### Avatar Buttons ########### 
class RBX_BUTTON_AVA(bpy.types.Operator):
    bl_label = "RBX_BUTTON_AVA"
    bl_idname = "object.rbx_button_ava"
    bl_options = {'REGISTER', 'UNDO'}
    rbx_ava : bpy.props.StringProperty(name= "Added") # type: ignore

    def execute(self, context):
        global rbx_anim_error
        global unhide_store
        scene = context.scene
        rbx_prefs = scene.rbx_prefs        
        rbx_ava = self.rbx_ava

        ava_list = [
                    'Blocky_ava',
                    'Round_male',
                    'Anime_ava'
                    ]

        if rbx_ava == 'avatar':     
            for x in range(len(ava_list)):
                if rbx_prefs.rbx_ava_enum == 'OP' + str(x+1):
                    ava_spwn = ava_list[x]   
            
            colls_before = set(bpy.data.collections)
            bpy.ops.wm.append(directory = glob_vars.addon_path + glob_vars.rbx_blend_file + glob_vars.ap_collection, filename =ava_spwn)
            
            # Clean up .000 suffixes from the newly spawned collection and its objects
            new_colls = set(bpy.data.collections) - colls_before
            for coll in new_colls:
                if '.' in coll.name:
                    coll.name = coll.name.split('.')[0]
                for obj in coll.objects:
                    if '.' in obj.name:
                        obj.name = obj.name.split('.')[0]
            
            bpy.context.view_layer.update()
            
        if rbx_ava == 'clear':
            selected = bpy.context.selected_objects
            active = bpy.context.view_layer.objects.active
            prop_lst = []
            
            bpy.ops.object.select_all(action='DESELECT')
            bpy.context.view_layer.objects.active = None
            
            for item in selected:
                bpy.data.objects[item.name].select_set(True)
                bpy.context.view_layer.objects.active = bpy.data.objects[item.name]
                
                props = bpy.data.objects[item.name].items()
       
                for x in props:
                    prop_lst.append(x[0])
                for prop in prop_lst:
                    bpy.ops.wm.properties_remove(data_path='object', property_name=prop)
                prop_lst.clear()
                bpy.ops.object.select_all(action='DESELECT')
                bpy.context.view_layer.objects.active = None
                
            for item in selected:
                bpy.data.objects[item.name].select_set(True)
                bpy.context.view_layer.objects.active = active
                
            bpy.context.view_layer.update()
            
            
        if rbx_ava == 'add_facs':
            selected = bpy.context.selected_objects
            
            if len(selected) != 1:
                self.report({'ERROR'}, "Select exactly 1 Head Mesh")
                return {'FINISHED'}
            
            obj = selected[0]
            if 'Head' not in obj.name:
                self.report({'ERROR'}, "Head Mesh should be selected")
                return {'FINISHED'}
            
            facs_properties = [
                ('Frame0', 'Neutral'),
                ('Frame1', 'Corrugator'),
                ('Frame2', 'ChinRaiserUpperLip'),
                ('Frame3', 'ChinRaiser'),
                ('Frame4', 'EyesLookDown'),
                ('Frame5', 'EyesLookLeft'),
                ('Frame6', 'EyesLookRight'),
                ('Frame7', 'EyesLookUp'),
                ('Frame8', 'Funneler'),
                ('Frame9', 'FlatPucker'),
                ('Frame10', 'JawDrop'),
                ('Frame11', 'JawLeft'),
                ('Frame12', 'JawRight'),
                ('Frame13', 'LowerLipSuck'),
                ('Frame14', 'LipPresser'),
                ('Frame15', 'LipsTogether'),
                ('Frame16', 'MouthLeft'),
                ('Frame17', 'MouthRight'),
                ('Frame18', 'Pucker'),
                ('Frame19', 'UpperLipSuck'),
                ('Frame20', 'LeftBrowLowerer'),
                ('Frame21', 'LeftCheekPuff'),
                ('Frame22', 'LeftCheekRaiser'),
                ('Frame23', 'LeftDimpler'),
                ('Frame24', 'LeftEyeClosed'),
                ('Frame25', 'LeftEyeUpperLidRaiser'),
                ('Frame26', 'LeftInnerBrowRaiser'),
                ('Frame27', 'LeftLipCornerDown'),
                ('Frame28', 'LeftLipCornerPuller'),
                ('Frame29', 'LeftLowerLipDepressor'),
                ('Frame30', 'LeftLipStretcher'),
                ('Frame31', 'LeftNoseWrinkler'),
                ('Frame32', 'LeftOuterBrowRaiser'),
                ('Frame33', 'LeftUpperLipRaiser'),
                ('Frame34', 'RightBrowLowerer'),
                ('Frame35', 'RightCheekPuff'),
                ('Frame36', 'RightCheekRaiser'),
                ('Frame37', 'RightDimpler'),
                ('Frame38', 'RightEyeClosed'),
                ('Frame39', 'RightEyeUpperLidRaiser'),
                ('Frame40', 'RightInnerBrowRaiser'),
                ('Frame41', 'RightLipCornerDown'),
                ('Frame42', 'RightLipCornerPuller'),
                ('Frame43', 'RightLowerLipDepressor'),
                ('Frame44', 'RightLipStretcher'),
                ('Frame45', 'RightNoseWrinkler'),
                ('Frame46', 'RightOuterBrowRaiser'),
                ('Frame47', 'RightUpperLipRaiser'),
                ('Frame100', 'TongueDown'),
                ('Frame101', 'TongueOut'),
                ('Frame102', 'TongueUp'),
                ('Frame110', 'JawDrop_TongueDown'),
                ('Frame111', 'JawDrop_TongueOut'),
                ('Frame112', 'JawDrop_TongueUp'),
                ('Frame113', 'TongueDown_TongueOut'),
                ('Frame114', 'TongueOut_TongueUp'),
                ('Frame130', 'JawDrop_TongueDown_TongueOut'),
                ('Frame131', 'JawDrop_TongueOut_TongueUp'),
                ('Frame200', 'Funneler_JawDrop'),
                ('Frame201', 'Funneler_Pucker'),
                ('Frame202', 'JawDrop_LowerLipSuck'),
                ('Frame203', 'JawDrop_Pucker'),
                ('Frame204', 'LipsTogether_Pucker'),
                ('Frame205', 'EyesLookDown_EyesLookLeft'),
                ('Frame206', 'EyesLookDown_EyesLookRight'),
                ('Frame207', 'EyesLookLeft_EyesLookUp'),
                ('Frame208', 'EyesLookRight_EyesLookUp'),
                ('Frame209', 'LeftCheekRaiser_LeftEyeClosed'),
                ('Frame210', 'LeftEyeClosed_EyesLookDown'),
                ('Frame211', 'LeftEyeClosed_EyesLookLeft'),
                ('Frame212', 'LeftEyeClosed_EyesLookRight'),
                ('Frame213', 'LeftEyeClosed_EyesLookUp'),
                ('Frame214', 'EyesLookUp_LeftEyeUpperLidRaiser'),
                ('Frame215', 'JawDrop_LeftLipCornerPuller'),
                ('Frame216', 'JawDrop_LeftLowerLipDepressor'),
                ('Frame217', 'JawDrop_LeftLipStretcher'),
                ('Frame218', 'JawDrop_LeftUpperLipRaiser'),
                ('Frame219', 'LeftLipCornerPuller_LeftLowerLipDepressor'),
                ('Frame220', 'LeftLipCornerPuller_LeftLipStretcher'),
                ('Frame221', 'LeftLipCornerPuller_Pucker'),
                ('Frame222', 'LeftLipCornerPuller_LeftUpperLipRaiser'),
                ('Frame223', 'LeftLowerLipDepressor_Pucker'),
                ('Frame224', 'LeftLipStretcher_LeftUpperLipRaiser'),
                ('Frame225', 'Pucker_LeftUpperLipRaiser'),
                ('Frame226', 'RightCheekRaiser_RightEyeClosed'),
                ('Frame227', 'RightEyeClosed_EyesLookDown'),
                ('Frame228', 'RightEyeClosed_EyesLookLeft'),
                ('Frame229', 'RightEyeClosed_EyesLookRight'),
                ('Frame230', 'RightEyeClosed_EyesLookUp'),
                ('Frame231', 'EyesLookUp_RightEyeUpperLidRaiser'),
                ('Frame232', 'JawDrop_RightLipCornerPuller'),
                ('Frame233', 'JawDrop_RightLowerLipDepressor'),
                ('Frame234', 'JawDrop_RightLipStretcher'),
                ('Frame235', 'JawDrop_RightUpperLipRaiser'),
                ('Frame236', 'RightLipCornerPuller_RightLowerLipDepressor'),
                ('Frame237', 'RightLipCornerPuller_RightLipStretcher'),
                ('Frame238', 'RightLipCornerPuller_Pucker'),
                ('Frame239', 'RightLipCornerPuller_RightUpperLipRaiser'),
                ('Frame240', 'RightLowerLipDepressor_Pucker'),
                ('Frame241', 'RightLipStretcher_RightUpperLipRaiser'),
                ('Frame242', 'Pucker_RightUpperLipRaiser'),
                ('Frame243', 'LeftBrowLowerer_LeftEyeClosed'),
                ('Frame244', 'RightBrowLowerer_RightEyeClosed'),
                ('Frame245', 'LeftLipCornerDown_LeftLowerLipDepressor'),
                ('Frame246', 'RightLipCornerDown_RightLowerLipDepressor'),
                ('Frame247', 'LeftInnerBrowRaiser_LeftOuterBrowRaiser'),
                ('Frame248', 'RightInnerBrowRaiser_RightOuterBrowRaiser'),
                ('Frame300', 'Funneler_JawDrop_Pucker'),
                ('Frame301', 'JawDrop_LeftLowerLipDepressor_Pucker'),
                ('Frame302', 'JawDrop_Pucker_LeftUpperLipRaiser'),
                ('Frame303', 'JawDrop_RightLowerLipDepressor_Pucker'),
                ('Frame304', 'JawDrop_Pucker_RightUpperLipRaiser'),
                ('dropoff', 4.0),
                ('smoothness', 0.0),
                ('RootFaceJoint', 'DynamicHead'),
            ]
            
            for prop_name, prop_value in facs_properties:
                obj[prop_name] = prop_value
            
            bpy.context.view_layer.update()
            
            
        if rbx_ava == 'add_facs_anim':
            selected = bpy.context.selected_objects
            
            if len(selected) != 1 or selected[0].type != 'ARMATURE':
                self.report({'ERROR'}, "Select exactly 1 Armature")
                return {'FINISHED'}
                
            target_rig = selected[0]
            colls_before = set(bpy.data.collections)
            objs_before = set(bpy.data.objects)
            
            # Append the template armature
            ava_spwn = 'Blocky_ava'
            try:
                bpy.ops.wm.append(directory = glob_vars.addon_path + glob_vars.rbx_blend_file + "/Collection/", filename = ava_spwn)
            except Exception as e:
                self.report({'ERROR'}, f"Failed to append: {e}")
                return {'FINISHED'}
                
            new_objs = set(bpy.data.objects) - objs_before
            
            # Find the appended armature and its animation
            template_rig = None
            for obj in new_objs:
                if obj.type == 'ARMATURE' and obj.animation_data and obj.animation_data.action:
                    template_rig = obj
                    break
                    
            if template_rig and template_rig.animation_data.action:
                template_action = template_rig.animation_data.action
                
                # Check for missing bones
                anim_bones = set()
                for fc in template_action.fcurves:
                    if fc.data_path.startswith("pose.bones"):
                        try:
                            # Safely extract bone name whether it uses single or double quotes
                            bone_name = fc.data_path.split('[')[1].split(']')[0].strip('\'"')
                            anim_bones.add(bone_name)
                        except Exception:
                            pass

                # The template animation contains the full body, but FACS is only for the face.
                # Ignore missing standard R15 body parts.
                ignored_parts = {
                    "LeftUpperArm", "LeftLowerArm", "LeftHand",
                    "RightUpperArm", "RightLowerArm", "RightHand",
                    "LeftUpperLeg", "LeftLowerLeg", "LeftFoot",
                    "RightUpperLeg", "RightLowerLeg", "RightFoot",
                    "UpperTorso", "LowerTorso", "Head", "HumanoidRootPart"
                }

                missing_bones = set()
                for b in anim_bones:
                    if b not in target_rig.pose.bones and b not in ignored_parts:
                        missing_bones.add(b)
                
                # We only count FACS bones.
                facs_bones_expected = len([b for b in anim_bones if b not in ignored_parts])
                
                if len(missing_bones) > 0:
                    # If ALL FACS bones in the animation are missing from the rig, the names are fundamentally wrong/different
                    if len(missing_bones) == facs_bones_expected and facs_bones_expected > 0:
                        glob_vars.rbx_facs_anim_error = "Bones in face armature have wrong names."
                    else:
                        # Only SOME FACS bones are missing
                        glob_vars.rbx_facs_anim_error = "Some bones are missing in face armature."
                    print(f"DEBUG FACS ANIMATION: Missing bones: {missing_bones}")
                else:
                    glob_vars.rbx_facs_anim_error = None
                
                # Create a fresh action to avoid inherited Action Slot binding issues in Blender 4.3+
                new_action = bpy.data.actions.new(name="FACS_Animation")
                
                # Copy only bone poses and custom properties directly to fresh F-Curves
                for fc in template_action.fcurves:
                    if fc.data_path.startswith("pose.bones") or fc.data_path.startswith('["'):
                        new_fc = new_action.fcurves.new(data_path=fc.data_path, index=fc.array_index)
                        
                        # Copy keyframes
                        for kp in fc.keyframe_points:
                            new_kp = new_fc.keyframe_points.insert(kp.co.x, kp.co.y, options={'FAST'})
                            new_kp.interpolation = kp.interpolation
                            new_kp.handle_left = kp.handle_left
                            new_kp.handle_left_type = kp.handle_left_type
                            new_kp.handle_right = kp.handle_right
                            new_kp.handle_right_type = kp.handle_right_type
                new_action.fcurves.update()

                # Assign the action to the target rig
                if not target_rig.animation_data:
                    target_rig.animation_data_create()
                else:
                    # Clear any NLA tracks to ensure the active action plays instantly
                    if target_rig.animation_data.nla_tracks:
                        for track in list(target_rig.animation_data.nla_tracks):
                            target_rig.animation_data.nla_tracks.remove(track)
                            
                target_rig.animation_data.action = new_action
                
                self.report({'INFO'}, "FACS Animation applied!")
            else:
                self.report({'ERROR'}, "Could not find animation data in template")
                
            # Clean up the appended items
            bpy.ops.object.select_all(action='DESELECT')
            for obj in new_objs:
                bpy.data.objects.remove(obj, do_unlink=True)
                
            new_colls = set(bpy.data.collections) - colls_before
            for coll in new_colls:
                bpy.data.collections.remove(coll)
                
            # Reselect target
            target_rig.select_set(True)
            bpy.context.view_layer.objects.active = target_rig
            bpy.context.view_layer.update()


        if rbx_ava == 'rename':
            objects = bpy.context.selected_objects
        
            for item in objects:
                if '.' in item.name:
                     new_name = item.name.split('.')[0]
                     item.name = new_name
            
            bpy.context.view_layer.update()
            
            
        if rbx_ava == 'hide':
            objects = bpy.context.selected_objects
            
            for item in objects:
                if '_Att' in item.name:
                    item.hide_viewport = True
                    unhide_store.append(item)
            
            bpy.context.view_layer.update()
            
            
        if rbx_ava == 'unhide':
           for item in unhide_store:
               item.hide_viewport = False

           unhide_store.clear()
           bpy.context.view_layer.update()
                   
            
        if rbx_ava == 'export':
            bpy.ops.export_scene.fbx('INVOKE_DEFAULT', path_mode='COPY', embed_textures=True, use_selection=True, object_types={'MESH', 'OTHER', 'EMPTY', 'ARMATURE'}, use_custom_props=True, add_leaf_bones=False, bake_anim=True, bake_anim_use_nla_strips=False, bake_anim_use_all_actions=True, bake_anim_force_startend_keying=False, bake_anim_simplify_factor=0)


        return {'FINISHED'}         