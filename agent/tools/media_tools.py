#!/usr/bin/env python
"""
media tools for the Reachy 2 robot.

This module provides tools for interacting with the media module of the Reachy 2 SDK.
"""

from typing import Dict, Any, List, Optional, Union, Tuple
from .base_tool import BaseTool
from agent.tools.connection_manager import get_reachy

class MediaTools(BaseTool):
    """Tools for interacting with the media module of the Reachy 2 SDK."""
    
    @classmethod
    def register_all_tools(cls) -> None:
        """Register all media tools."""
        cls.register_tool(
            name="media_camera_Camera___init__",
            func=cls.media_camera_Camera___init__,
            schema=cls.create_tool_schema(
                name="media_camera_Camera___init__",
                description="""Initialize a Camera instance.

This constructor sets up a camera instance by storing the camera's
information and gRPC video stub for accessing camera-related services.

Args:
    cam_info: An instance of `CameraFeatures` containing the camera's
        details, such as its name, capabilities, and settings.
    video_stub: A `VideoServiceStub` for making gRPC calls to the video
        service, enabling access to camera frames, parameters, and other
        camera-related functionality.""",
                parameters={'cam_info': {'type': 'string', 'description': "An instance of `CameraFeatures` containing the camera's"}, 'video_stub': {'type': 'string', 'description': 'A `VideoServiceStub` for making gRPC calls to the video'}},
                required=['cam_info', 'video_stub']
            )
        )
        cls.register_tool(
            name="media_camera_Camera_get_frame",
            func=cls.media_camera_Camera_get_frame,
            schema=cls.create_tool_schema(
                name="media_camera_Camera_get_frame",
                description="""Retrieve an RGB frame from the camera.

Args:
    view: The camera view to retrieve the frame from. Default is CameraView.LEFT.

Returns:
    A tuple containing the frame as a NumPy array in OpenCV format and the timestamp in nanoseconds.
    Returns None if no frame is retrieved.""",
                parameters={'view': {'type': 'string', 'description': 'The camera view to retrieve the frame from. Default is CameraView.LEFT.'}},
                required=['view']
            )
        )
        cls.register_tool(
            name="media_camera_Camera_get_compressed_frame",
            func=cls.media_camera_Camera_get_compressed_frame,
            schema=cls.create_tool_schema(
                name="media_camera_Camera_get_compressed_frame",
                description="""Retrieve an RGB frame in a JPEG format from the camera.

Args:
    view: The camera view to retrieve the frame from. Default is CameraView.LEFT.

Returns:
    A bytes array containing the jpeg frame and the timestamp in nanoseconds.
    Returns None if no frame is retrieved.""",
                parameters={'view': {'type': 'string', 'description': 'The camera view to retrieve the frame from. Default is CameraView.LEFT.'}},
                required=['view']
            )
        )
        cls.register_tool(
            name="media_camera_Camera_get_parameters",
            func=cls.media_camera_Camera_get_parameters,
            schema=cls.create_tool_schema(
                name="media_camera_Camera_get_parameters",
                description="""Retrieve camera parameters including intrinsic matrix.

Args:
    view: The camera view for which parameters should be retrieved. Default is CameraView.LEFT.

Returns:
    A tuple containing height, width, distortion model, distortion coefficients, intrinsic matrix,
    rotation matrix, and projection matrix. Returns None if no parameters are retrieved.""",
                parameters={'view': {'type': 'string', 'description': 'The camera view for which parameters should be retrieved. Default is CameraView.LEFT.'}},
                required=['view']
            )
        )
        cls.register_tool(
            name="media_camera_Camera_get_extrinsics",
            func=cls.media_camera_Camera_get_extrinsics,
            schema=cls.create_tool_schema(
                name="media_camera_Camera_get_extrinsics",
                description="""Retrieve the 4x4 extrinsic matrix of the camera.

Args:
    view: The camera view for which the extrinsic matrix should be retrieved. Default is CameraView.LEFT.

Returns:
    The extrinsic matrix as a NumPy array. Returns None if no matrix is retrieved.""",
                parameters={'view': {'type': 'string', 'description': 'The camera view for which the extrinsic matrix should be retrieved. Default is CameraView.LEFT.'}},
                required=['view']
            )
        )
        cls.register_tool(
            name="media_camera_Camera_pixel_to_world",
            func=cls.media_camera_Camera_pixel_to_world,
            schema=cls.create_tool_schema(
                name="media_camera_Camera_pixel_to_world",
                description="""Convert pixel coordinates to XYZ coordinate in Reachy coordinate system.

Args:
    u: The x-coordinate (pixel) in the camera view (horizontal axis, left-to-right).
    v: The y-coordinate (pixel) in the camera view (vertical axis, top-to-bottom).
    z_c: The depth value in meters at the given pixel. Default is 1.0.
    view: The camera view to use for the conversion. Default is CameraView.LEFT.

Returns:
    A NumPy array containing the [X, Y, Z] world coordinates in meters. Returns None if the conversion fails.""",
                parameters={'u': {'type': 'integer', 'description': 'The x-coordinate (pixel) in the camera view (horizontal axis, left-to-right).'}, 'v': {'type': 'integer', 'description': 'The y-coordinate (pixel) in the camera view (vertical axis, top-to-bottom).'}, 'z_c': {'type': 'number', 'description': 'The depth value in meters at the given pixel. Default is 1.0.'}, 'view': {'type': 'string', 'description': 'The camera view to use for the conversion. Default is CameraView.LEFT.'}},
                required=['u', 'v', 'z_c', 'view']
            )
        )
        cls.register_tool(
            name="media_camera_Camera___repr__",
            func=cls.media_camera_Camera___repr__,
            schema=cls.create_tool_schema(
                name="media_camera_Camera___repr__",
                description="""Clean representation of a RGB camera.""",
                parameters={},
                required=[]
            )
        )
        cls.register_tool(
            name="media_camera_DepthCamera_get_depth_frame",
            func=cls.media_camera_DepthCamera_get_depth_frame,
            schema=cls.create_tool_schema(
                name="media_camera_DepthCamera_get_depth_frame",
                description="""Retrieve a depth frame from the camera.

Args:
    view: The camera view to retrieve the depth frame from. Default is CameraView.DEPTH.

Returns:
    A tuple containing the depth frame as a NumPy array in 16-bit format and the timestamp in nanoseconds.
    Returns None if no frame is retrieved.""",
                parameters={'view': {'type': 'string', 'description': 'The camera view to retrieve the depth frame from. Default is CameraView.DEPTH.'}},
                required=['view']
            )
        )
        cls.register_tool(
            name="media_camera_manager_CameraManager___init__",
            func=cls.media_camera_manager_CameraManager___init__,
            schema=cls.create_tool_schema(
                name="media_camera_manager_CameraManager___init__",
                description="""Set up the camera manager module.

This initializes the gRPC channel for communicating with the camera service,
sets up logging, and prepares the available cameras.

Args:
    host: The host address for the gRPC service.
    port: The port number for the gRPC service.""",
                parameters={'host': {'type': 'string', 'description': 'The host address for the gRPC service.'}, 'port': {'type': 'integer', 'description': 'The port number for the gRPC service.'}},
                required=['host', 'port']
            )
        )
        cls.register_tool(
            name="media_camera_manager_CameraManager___repr__",
            func=cls.media_camera_manager_CameraManager___repr__,
            schema=cls.create_tool_schema(
                name="media_camera_manager_CameraManager___repr__",
                description="""Clean representation of a reachy cameras.""",
                parameters={},
                required=[]
            )
        )
        cls.register_tool(
            name="media_camera_manager_CameraManager_initialize_cameras",
            func=cls.media_camera_manager_CameraManager_initialize_cameras,
            schema=cls.create_tool_schema(
                name="media_camera_manager_CameraManager_initialize_cameras",
                description="""Manually re-initialize cameras.

This method can be used to reinitialize the camera setup if changes occur
or new cameras are connected.""",
                parameters={},
                required=[]
            )
        )
        cls.register_tool(
            name="media_camera_manager_CameraManager_teleop",
            func=cls.media_camera_manager_CameraManager_teleop,
            schema=cls.create_tool_schema(
                name="media_camera_manager_CameraManager_teleop",
                description="""Retrieve the teleop camera.

Returns:
    The teleop Camera object if it is initialized; otherwise, logs an error
    and returns None.""",
                parameters={},
                required=[]
            )
        )
        cls.register_tool(
            name="media_camera_manager_CameraManager_depth",
            func=cls.media_camera_manager_CameraManager_depth,
            schema=cls.create_tool_schema(
                name="media_camera_manager_CameraManager_depth",
                description="""Retrieve the depth camera.

Returns:
    The DepthCamera object if it is initialized; otherwise, logs an error
    and returns None.""",
                parameters={},
                required=[]
            )
        )
        cls.register_tool(
            name="media_audio_Audio___init__",
            func=cls.media_audio_Audio___init__,
            schema=cls.create_tool_schema(
                name="media_audio_Audio___init__",
                description="""Set up the audio module.

This initializes the gRPC channel for communicating with the audio service.

Args:
    host: The host address for the gRPC service.
    port: The port number for the gRPC service.""",
                parameters={'host': {'type': 'string', 'description': 'The host address for the gRPC service.'}, 'port': {'type': 'integer', 'description': 'The port number for the gRPC service.'}},
                required=['host', 'port']
            )
        )
        cls.register_tool(
            name="media_audio_Audio_upload_audio_file",
            func=cls.media_audio_Audio_upload_audio_file,
            schema=cls.create_tool_schema(
                name="media_audio_Audio_upload_audio_file",
                description="""Upload an audio file to the robot.

This method uploads an audio file to the robot. The audio file is stored in a temporary folder on the robot
and is deleted when the robot is turned off.

Args:
    path: The path to the audio file to upload.""",
                parameters={'path': {'type': 'string', 'description': 'The path to the audio file to upload.'}},
                required=['path']
            )
        )
        cls.register_tool(
            name="media_audio_Audio_download_audio_file",
            func=cls.media_audio_Audio_download_audio_file,
            schema=cls.create_tool_schema(
                name="media_audio_Audio_download_audio_file",
                description="""Download an audio file from the robot.

Args:
    name: The name of the audio file to download.
    path: The folder to save the downloaded audio file.""",
                parameters={'name': {'type': 'string', 'description': 'The name of the audio file to download.'}, 'path': {'type': 'string', 'description': 'The folder to save the downloaded audio file.'}},
                required=['name', 'path']
            )
        )
        cls.register_tool(
            name="media_audio_Audio_get_audio_files",
            func=cls.media_audio_Audio_get_audio_files,
            schema=cls.create_tool_schema(
                name="media_audio_Audio_get_audio_files",
                description="""Get audio files from the robot.

This method retrieves the list of audio files stored on the robot.""",
                parameters={},
                required=[]
            )
        )
        cls.register_tool(
            name="media_audio_Audio_remove_audio_file",
            func=cls.media_audio_Audio_remove_audio_file,
            schema=cls.create_tool_schema(
                name="media_audio_Audio_remove_audio_file",
                description="""Remove an audio file from the robot.

This method removes an audio file from the robot.

Args:
    name: The name of the audio file to remove.""",
                parameters={'name': {'type': 'string', 'description': 'The name of the audio file to remove.'}},
                required=['name']
            )
        )
        cls.register_tool(
            name="media_audio_Audio_play_audio_file",
            func=cls.media_audio_Audio_play_audio_file,
            schema=cls.create_tool_schema(
                name="media_audio_Audio_play_audio_file",
                description="""Play an audio file on the robot.

This method plays an audio file on the robot.

Args:
    name: The name of the audio file to play.""",
                parameters={'name': {'type': 'string', 'description': 'The name of the audio file to play.'}},
                required=['name']
            )
        )
        cls.register_tool(
            name="media_audio_Audio_stop_playing",
            func=cls.media_audio_Audio_stop_playing,
            schema=cls.create_tool_schema(
                name="media_audio_Audio_stop_playing",
                description="""Stop playing audio on the robot.

This method stops the audio that is currently playing on the robot.""",
                parameters={},
                required=[]
            )
        )
        cls.register_tool(
            name="media_audio_Audio_record_audio",
            func=cls.media_audio_Audio_record_audio,
            schema=cls.create_tool_schema(
                name="media_audio_Audio_record_audio",
                description="""Record audio on the robot.

This method records audio on the robot.

Args:
    name: name of the audio file. The extension defines the encoding. Ony ogg is supported.
    duration_secs: duration of the recording in seconds.""",
                parameters={'name': {'type': 'string', 'description': 'name of the audio file. The extension defines the encoding. Ony ogg is supported.'}, 'duration_secs': {'type': 'number', 'description': 'duration of the recording in seconds.'}},
                required=['name', 'duration_secs']
            )
        )
        cls.register_tool(
            name="media_audio_Audio_stop_recording",
            func=cls.media_audio_Audio_stop_recording,
            schema=cls.create_tool_schema(
                name="media_audio_Audio_stop_recording",
                description="""Stop recording audio on the robot.

This method stops the audio recording on the robot.""",
                parameters={},
                required=[]
            )
        )

    @classmethod
    def media_camera_Camera___init__(cls, cam_info, video_stub) -> Dict[str, Any]:
        """Initialize a Camera instance.
        
        This constructor sets up a camera instance by storing the camera's
        information and gRPC video stub for accessing camera-related services.
        
        Args:
            cam_info: An instance of `CameraFeatures` containing the camera's
                details, such as its name, capabilities, and settings.
            video_stub: A `VideoServiceStub` for making gRPC calls to the video
                service, enabling access to camera frames, parameters, and other
                camera-related functionality."""
        try:
            # Get Reachy connection
            reachy = get_reachy()
            
            # Get the target object
            obj = getattr(reachy, 'camera')

            # Call the function with parameters
            result = obj.Camera___init__(cam_info, video_stub)

            return {
                "success": True,
                "result": result
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }


    @classmethod
    def media_camera_Camera_get_frame(cls, view) -> Dict[str, Any]:
        """Retrieve an RGB frame from the camera.
        
        Args:
            view: The camera view to retrieve the frame from. Default is CameraView.LEFT.
        
        Returns:
            A tuple containing the frame as a NumPy array in OpenCV format and the timestamp in nanoseconds.
            Returns None if no frame is retrieved."""
        try:
            # Get Reachy connection
            reachy = get_reachy()
            
            # Get the target object
            obj = getattr(reachy, 'camera')

            # Call the function with parameters
            result = obj.Camera_get_frame(view)

            return {
                "success": True,
                "result": result
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }


    @classmethod
    def media_camera_Camera_get_compressed_frame(cls, view) -> Dict[str, Any]:
        """Retrieve an RGB frame in a JPEG format from the camera.
        
        Args:
            view: The camera view to retrieve the frame from. Default is CameraView.LEFT.
        
        Returns:
            A bytes array containing the jpeg frame and the timestamp in nanoseconds.
            Returns None if no frame is retrieved."""
        try:
            # Get Reachy connection
            reachy = get_reachy()
            
            # Get the target object
            obj = getattr(reachy, 'camera')

            # Call the function with parameters
            result = obj.Camera_get_compressed_frame(view)

            return {
                "success": True,
                "result": result
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }


    @classmethod
    def media_camera_Camera_get_parameters(cls, view) -> Dict[str, Any]:
        """Retrieve camera parameters including intrinsic matrix.
        
        Args:
            view: The camera view for which parameters should be retrieved. Default is CameraView.LEFT.
        
        Returns:
            A tuple containing height, width, distortion model, distortion coefficients, intrinsic matrix,
            rotation matrix, and projection matrix. Returns None if no parameters are retrieved."""
        try:
            # Get Reachy connection
            reachy = get_reachy()
            
            # Get the target object
            obj = getattr(reachy, 'camera')

            # Call the function with parameters
            result = obj.Camera_get_parameters(view)

            return {
                "success": True,
                "result": result
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }


    @classmethod
    def media_camera_Camera_get_extrinsics(cls, view) -> Dict[str, Any]:
        """Retrieve the 4x4 extrinsic matrix of the camera.
        
        Args:
            view: The camera view for which the extrinsic matrix should be retrieved. Default is CameraView.LEFT.
        
        Returns:
            The extrinsic matrix as a NumPy array. Returns None if no matrix is retrieved."""
        try:
            # Get Reachy connection
            reachy = get_reachy()
            
            # Get the target object
            obj = getattr(reachy, 'camera')

            # Call the function with parameters
            result = obj.Camera_get_extrinsics(view)

            return {
                "success": True,
                "result": result
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }


    @classmethod
    def media_camera_Camera_pixel_to_world(cls, u, v, z_c, view) -> Dict[str, Any]:
        """Convert pixel coordinates to XYZ coordinate in Reachy coordinate system.
        
        Args:
            u: The x-coordinate (pixel) in the camera view (horizontal axis, left-to-right).
            v: The y-coordinate (pixel) in the camera view (vertical axis, top-to-bottom).
            z_c: The depth value in meters at the given pixel. Default is 1.0.
            view: The camera view to use for the conversion. Default is CameraView.LEFT.
        
        Returns:
            A NumPy array containing the [X, Y, Z] world coordinates in meters. Returns None if the conversion fails."""
        try:
            # Get Reachy connection
            reachy = get_reachy()
            
            # Get the target object
            obj = getattr(reachy, 'camera')

            # Call the function with parameters
            result = obj.Camera_pixel_to_world(u, v, z_c, view)

            return {
                "success": True,
                "result": result
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }


    @classmethod
    def media_camera_Camera___repr__(cls, ) -> Dict[str, Any]:
        """Clean representation of a RGB camera."""
        try:
            # Get Reachy connection
            reachy = get_reachy()
            
            # Get the target object
            obj = getattr(reachy, 'camera')

            # Call the function with parameters
            result = obj.Camera___repr__()

            return {
                "success": True,
                "result": result
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }


    @classmethod
    def media_camera_DepthCamera_get_depth_frame(cls, view) -> Dict[str, Any]:
        """Retrieve a depth frame from the camera.
        
        Args:
            view: The camera view to retrieve the depth frame from. Default is CameraView.DEPTH.
        
        Returns:
            A tuple containing the depth frame as a NumPy array in 16-bit format and the timestamp in nanoseconds.
            Returns None if no frame is retrieved."""
        try:
            # Get Reachy connection
            reachy = get_reachy()
            
            # Get the target object
            obj = getattr(reachy, 'camera')

            # Call the function with parameters
            result = obj.DepthCamera_get_depth_frame(view)

            return {
                "success": True,
                "result": result
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }


    @classmethod
    def media_camera_manager_CameraManager___init__(cls, host, port) -> Dict[str, Any]:
        """Set up the camera manager module.
        
        This initializes the gRPC channel for communicating with the camera service,
        sets up logging, and prepares the available cameras.
        
        Args:
            host: The host address for the gRPC service.
            port: The port number for the gRPC service."""
        try:
            # Get Reachy connection
            reachy = get_reachy()
            
            # Get the target object
            obj = getattr(reachy, 'camera')

            # Call the function with parameters
            result = obj.manager_CameraManager___init__(host, port)

            return {
                "success": True,
                "result": result
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }


    @classmethod
    def media_camera_manager_CameraManager___repr__(cls, ) -> Dict[str, Any]:
        """Clean representation of a reachy cameras."""
        try:
            # Get Reachy connection
            reachy = get_reachy()
            
            # Get the target object
            obj = getattr(reachy, 'camera')

            # Call the function with parameters
            result = obj.manager_CameraManager___repr__()

            return {
                "success": True,
                "result": result
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }


    @classmethod
    def media_camera_manager_CameraManager_initialize_cameras(cls, ) -> Dict[str, Any]:
        """Manually re-initialize cameras.
        
        This method can be used to reinitialize the camera setup if changes occur
        or new cameras are connected."""
        try:
            # Get Reachy connection
            reachy = get_reachy()
            
            # Get the target object
            obj = getattr(reachy, 'camera')

            # Call the function with parameters
            result = obj.manager_CameraManager_initialize_cameras()

            return {
                "success": True,
                "result": result
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }


    @classmethod
    def media_camera_manager_CameraManager_teleop(cls, ) -> Dict[str, Any]:
        """Retrieve the teleop camera.
        
        Returns:
            The teleop Camera object if it is initialized; otherwise, logs an error
            and returns None."""
        try:
            # Get Reachy connection
            reachy = get_reachy()
            
            # Get the target object
            obj = getattr(reachy, 'camera')

            # Call the function with parameters
            result = obj.manager_CameraManager_teleop()

            return {
                "success": True,
                "result": result
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }


    @classmethod
    def media_camera_manager_CameraManager_depth(cls, ) -> Dict[str, Any]:
        """Retrieve the depth camera.
        
        Returns:
            The DepthCamera object if it is initialized; otherwise, logs an error
            and returns None."""
        try:
            # Get Reachy connection
            reachy = get_reachy()
            
            # Get the target object
            obj = getattr(reachy, 'camera')

            # Call the function with parameters
            result = obj.manager_CameraManager_depth()

            return {
                "success": True,
                "result": result
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }


    @classmethod
    def media_audio_Audio___init__(cls, host, port) -> Dict[str, Any]:
        """Set up the audio module.
        
        This initializes the gRPC channel for communicating with the audio service.
        
        Args:
            host: The host address for the gRPC service.
            port: The port number for the gRPC service."""
        try:
            # Get Reachy connection
            reachy = get_reachy()
            
            # Get the target object
            obj = getattr(reachy, 'audio')

            # Call the function with parameters
            result = obj.Audio___init__(host, port)

            return {
                "success": True,
                "result": result
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }


    @classmethod
    def media_audio_Audio_upload_audio_file(cls, path) -> Dict[str, Any]:
        """Upload an audio file to the robot.
        
        This method uploads an audio file to the robot. The audio file is stored in a temporary folder on the robot
        and is deleted when the robot is turned off.
        
        Args:
            path: The path to the audio file to upload."""
        try:
            # Get Reachy connection
            reachy = get_reachy()
            
            # Get the target object
            obj = getattr(reachy, 'audio')

            # Call the function with parameters
            result = obj.Audio_upload_audio_file(path)

            return {
                "success": True,
                "result": result
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }


    @classmethod
    def media_audio_Audio_download_audio_file(cls, name, path) -> Dict[str, Any]:
        """Download an audio file from the robot.
        
        Args:
            name: The name of the audio file to download.
            path: The folder to save the downloaded audio file."""
        try:
            # Get Reachy connection
            reachy = get_reachy()
            
            # Get the target object
            obj = getattr(reachy, 'audio')

            # Call the function with parameters
            result = obj.Audio_download_audio_file(name, path)

            return {
                "success": True,
                "result": result
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }


    @classmethod
    def media_audio_Audio_get_audio_files(cls, ) -> Dict[str, Any]:
        """Get audio files from the robot.
        
        This method retrieves the list of audio files stored on the robot."""
        try:
            # Get Reachy connection
            reachy = get_reachy()
            
            # Get the target object
            obj = getattr(reachy, 'audio')

            # Call the function with parameters
            result = obj.Audio_get_audio_files()

            return {
                "success": True,
                "result": result
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }


    @classmethod
    def media_audio_Audio_remove_audio_file(cls, name) -> Dict[str, Any]:
        """Remove an audio file from the robot.
        
        This method removes an audio file from the robot.
        
        Args:
            name: The name of the audio file to remove."""
        try:
            # Get Reachy connection
            reachy = get_reachy()
            
            # Get the target object
            obj = getattr(reachy, 'audio')

            # Call the function with parameters
            result = obj.Audio_remove_audio_file(name)

            return {
                "success": True,
                "result": result
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }


    @classmethod
    def media_audio_Audio_play_audio_file(cls, name) -> Dict[str, Any]:
        """Play an audio file on the robot.
        
        This method plays an audio file on the robot.
        
        Args:
            name: The name of the audio file to play."""
        try:
            # Get Reachy connection
            reachy = get_reachy()
            
            # Get the target object
            obj = getattr(reachy, 'audio')

            # Call the function with parameters
            result = obj.Audio_play_audio_file(name)

            return {
                "success": True,
                "result": result
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }


    @classmethod
    def media_audio_Audio_stop_playing(cls, ) -> Dict[str, Any]:
        """Stop playing audio on the robot.
        
        This method stops the audio that is currently playing on the robot."""
        try:
            # Get Reachy connection
            reachy = get_reachy()
            
            # Get the target object
            obj = getattr(reachy, 'audio')

            # Call the function with parameters
            result = obj.Audio_stop_playing()

            return {
                "success": True,
                "result": result
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }


    @classmethod
    def media_audio_Audio_record_audio(cls, name, duration_secs) -> Dict[str, Any]:
        """Record audio on the robot.
        
        This method records audio on the robot.
        
        Args:
            name: name of the audio file. The extension defines the encoding. Ony ogg is supported.
            duration_secs: duration of the recording in seconds."""
        try:
            # Get Reachy connection
            reachy = get_reachy()
            
            # Get the target object
            obj = getattr(reachy, 'audio')

            # Call the function with parameters
            result = obj.Audio_record_audio(name, duration_secs)

            return {
                "success": True,
                "result": result
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }


    @classmethod
    def media_audio_Audio_stop_recording(cls, ) -> Dict[str, Any]:
        """Stop recording audio on the robot.
        
        This method stops the audio recording on the robot."""
        try:
            # Get Reachy connection
            reachy = get_reachy()
            
            # Get the target object
            obj = getattr(reachy, 'audio')

            # Call the function with parameters
            result = obj.Audio_stop_recording()

            return {
                "success": True,
                "result": result
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
