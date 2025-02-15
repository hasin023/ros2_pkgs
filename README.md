# ros2_pkgs
To create a pkg, we need to follow these steps

```bash
cd /home/ros2_ws/src

ros2 pkg create --build-type ament_python --license Apache-2.0 --node-name <node_name> <package_name>
```

We need to ensure that all our dependencies are installed inside our workspace, before we are building our pkg

```bash
rosdep install -i --from-path src --rosdistro humble -y
```

Next, we need to build the pkg

```bash
cd /home/ros2_ws

colcon build
```

If we have any previously built pkg that we want to get rid of, we simply need to remove the /build /install /log directories.

```bash
rm -rf src/<package_name>

rm -rf build/ install/ log/

colcon build

colcon build --packages-select <package_name>      // If we want to build a specific pkg
```

If the build fails, we might need to downgrade our python setuptools version.

```bash
apt install python3-pip

pip3 list | grep setuptools

pip3 install setuptools==58.2.0
```

Once the pkg is build, we can find it inside the install directory, we need to first source the local setup script inside the install directory.

```bash
source install/local_setup.bash
```

Finally, we can now run the pkg

```bash
ros2 run <package_name> <node_name>
```
