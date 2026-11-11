from launch import LaunchDescription
from launch.actions import (
    DeclareLaunchArgument,
    IncludeLaunchDescription,
)
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import Command, FindExecutable, LaunchConfiguration, PathJoinSubstitution
from launch_ros.actions import Node
from launch_ros.parameter_descriptions import ParameterValue
from launch_ros.substitutions import FindPackageShare


def generate_launch_description():
    use_sim_time = LaunchConfiguration("use_sim_time")
    gz_args = LaunchConfiguration("gz_args")

    package_share = FindPackageShare("robot_description")
    xacro_file = PathJoinSubstitution([package_share, "urdf", "drone.urdf.xacro"])

    robot_description = {
        "robot_description": ParameterValue(
            Command([FindExecutable(name="xacro"), " ", xacro_file]),
            value_type=str,
        )
    }

    # === 1. Gazebo Sim ===
    gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            PathJoinSubstitution(
                [FindPackageShare("ros_gz_sim"), "launch", "gz_sim.launch.py"]
            )
        ),
        launch_arguments={"gz_args": gz_args}.items(),
    )

    # === 2. robot_state_publisher ===
    robot_state_publisher = Node(
        package="robot_state_publisher",
        executable="robot_state_publisher",
        name="robot_state_publisher",
        output="screen",
        parameters=[robot_description, {"use_sim_time": use_sim_time}],
    )

    # === 3. Bridge ROS <-> Gazebo ===
    # NOTE : /joint_states a été retiré (plus de broadcaster).
    # NOTE : /odom a été retiré (PX4 fournira l'odométrie).
    ros_gz_bridge = Node(
        package="ros_gz_bridge",
        executable="parameter_bridge",
        name="ros_gz_bridge",
        output="screen",
        parameters=[{"use_sim_time": use_sim_time}],
        arguments=[
            "/clock@rosgraph_msgs/msg/Clock[gz.msgs.Clock",
            "/imu@sensor_msgs/msg/Imu[gz.msgs.IMU",
            "/camera/image_raw@sensor_msgs/msg/Image[gz.msgs.Image",
            "/camera/camera_info@sensor_msgs/msg/CameraInfo[gz.msgs.CameraInfo",
            "/tf@tf2_msgs/msg/TFMessage[gz.msgs.Pose_V",
        ],
    )

    # === 4. Spawn du drone ===
    spawn_drone = Node(
        package="ros_gz_sim",
        executable="create",
        name="spawn_drone",
        output="screen",
        arguments=[
            "-topic", "robot_description",
            "-name", "air3s",
            "-x", "0.0", "-y", "0.0", "-z", "0.5",
        ],
    )

    return LaunchDescription(
        [
            DeclareLaunchArgument(
                "use_sim_time",
                default_value="true",
                description="Use Gazebo simulation time.",
            ),
            DeclareLaunchArgument(
                "gz_args",
                default_value="-r -v 4 empty.sdf",
                description="Arguments passed to Gazebo Sim.",
            ),
            gazebo,
            ros_gz_bridge,
            robot_state_publisher,
            spawn_drone,
        ]
    )