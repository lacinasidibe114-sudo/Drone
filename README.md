<div align="center">

<img src="https://capsule-render.vercel.app/api?type=waving&height=210&color=0:070A10,55:0B2A33,100:0FB5A0&text=Drone%20Simulation&fontColor=E8F3F1&fontSize=46&fontAlignY=36&desc=Quadrirotor%20%C2%B7%20Gazebo%20%C2%B7%20PX4%20SITL&descAlignY=57&descSize=17&animation=fadeIn" alt="Drone Simulation : Quadrirotor · Gazebo · PX4 SITL" width="100%" />

<p>
  <img src="https://img.shields.io/badge/ROS%202-Humble-22314E?style=flat-square&logo=ros&logoColor=white" alt="ROS 2 Humble" />
  <img src="https://img.shields.io/badge/Gazebo-Fortress-F58113?style=flat-square" alt="Gazebo Fortress" />
  <img src="https://img.shields.io/badge/PX4-SITL-1F2937?style=flat-square" alt="PX4 SITL" />
  <img src="https://img.shields.io/badge/ros2__control-hardware-0F766E?style=flat-square" alt="ros2_control hardware" />
  <img src="https://img.shields.io/badge/Statut-en%20cours-D97706?style=flat-square" alt="Statut en cours" />
</p>

<p><b><a href="https://lacinasidibe114-sudo.github.io/lacina-portfolio/">Portfolio</a> · <a href="https://github.com/lacinasidibe114-sudo">Tous mes projets</a></b></p>

</div>

## En bref

Modélisation et simulation d'un **quadrirotor de type DJI Air 3S** sous ROS 2 et Gazebo, avec deux modes de commande :

- **`ros2_control`** : les quatre hélices sont des articulations pilotées en vitesse par un `ForwardCommandController`, pour expérimenter la commande bas niveau.
- **PX4 (SITL)** : l'autopilote PX4 prend en charge la stabilisation et l'odométrie, ROS 2 reçoit les capteurs par `ros_gz_bridge`.

> **Statut : en cours.** Le modèle, les capteurs et les deux modes de lancement sont en place ; l'intégration complète de PX4 (commande de mission depuis ROS 2) est la prochaine étape.

## Modèle

| Élément | Détail |
|---|---|
| Fuselage | 0,40 kg, inerties renseignées, coque, bras et carénages en primitives |
| Propulsion | 4 hélices `prop_fl/fr/rl/rr_joint` pilotées en vitesse |
| Capteurs | Caméra sur nacelle (`/camera/image_raw`, `/camera/camera_info`) et IMU (`/imu`) |
| Simulateur | Gazebo Fortress (`ignition-gazebo` 6) via `ros_gz_sim` |

## Architecture

```mermaid
flowchart LR
    XACRO["drone.urdf.xacro<br/>+ plugin.xacro / plugin_px4.xacro"] --> RSP["robot_state_publisher"]
    XACRO --> GZ["Gazebo Fortress"]
    subgraph M1["Mode ros2_control"]
        CM["controller_manager · 100 Hz"] --> FWD["motor_velocity_controller<br/>ForwardCommandController"]
    end
    subgraph M2["Mode PX4 SITL"]
        PX4["PX4 Autopilot"]
    end
    FWD --> GZ
    PX4 --> GZ
    GZ -->|ros_gz_bridge| TOP(["/clock · /imu · /camera/image_raw · /tf"])
```

## Démarrage rapide

```bash
git clone https://github.com/lacinasidibe114-sudo/Drone.git ~/drone_ws
cd ~/drone_ws
rosdep install --from-paths src -y --ignore-src
colcon build && source install/setup.bash

# Mode ros2_control : commande directe des hélices
ros2 launch robot_description gazebo.launch.py
ros2 topic pub /motor_velocity_controller/commands std_msgs/msg/Float64MultiArray "{data: [400.0, 400.0, 400.0, 400.0]}"

# Mode PX4 : capteurs exposés à ROS 2, PX4 gère le vol
ros2 launch robot_description gazebo_px4.launch.py
```

## Feuille de route

- [x] Modèle URDF/Xacro avec inerties, caméra et IMU
- [x] Simulation Gazebo et contrôleur de vitesse des hélices
- [x] Pont ROS 2 ↔ Gazebo pour les capteurs
- [ ] Liaison PX4 ↔ ROS 2 (uXRCE-DDS) et envoi de consignes de position
- [ ] Mission autonome : décollage, suivi de points de passage, atterrissage

---

<div align="center">

<img src="https://capsule-render.vercel.app/api?type=waving&section=footer&height=110&color=0:0FB5A0,45:0B2A33,100:070A10" width="100%" alt="" />

<sub><b>Lacina Sidibé</b> · Élève-ingénieur Robotique &amp; IA · <a href="https://lacinasidibe114-sudo.github.io/lacina-portfolio/">Portfolio</a> · en recherche de PFE 2027</sub>

</div>
