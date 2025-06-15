# skybox

This repository aims to create skyboxes from the cubemaps and images procedurally generated from noise using python and panda3D.  
The noise images, cubemaps and cloud cover images were created using programs from [NoiseTexture](https://github.com/taKana671/NoiseTexture) and its submodule [texture_generator](https://github.com/taKana671/texture_generator).  

# Requirements
* Panda3D 1.10.15
  
# Environment
* Python 3.12
* Windows11

# Skybox Demo

![Image](https://github.com/user-attachments/assets/9b506349-66a4-4370-b1a1-ffa344319a78)
<br>
### Clone this repository with submodule.
```
git clone --recursive https://github.com/taKana671/skybox.git
```

### Skybox from cubemap
Skybox image files bcreated with texture_generator must be renamed in advance.

<table>
    <tr>
      <th>before</th>
      <th>after</th>
    </tr>
    <tr>
      <th>img_front.png</th>
      <th>img_2.png</th>
    </tr>
    <tr>
      <th>img_right.png</th>
      <th>img_0.png</th>
    </tr>
    <tr>
      <th>img_back.png</th>
      <th>img_3.png</th>
    </tr>
    <tr>
      <th>img_left.png</th>
      <th>img_1.png</th>
    </tr>
    <tr>
      <th>img_top.png</th>
      <th>img_4.png</th>
    </tr>
    <tr>
      <th>img_bottom.png</th>
      <th>img_5.png</th>
    </tr>
</table>    
    
```
# skybox using a cubemap
>>>python skybox_demo_cubemap.py

# skybox using a cubemap converted from sphere map
>>>python skybox_demo_spheremap.py
```

### Skybox from display region

```
>>>python skybox_demo_displayregion.py
```

### Sphere sky from sphere map

```
>>>python spheresky_demo_spheremap.py
```

# Controls:
* Press [Esc] to quit.
* Press [up arrow] key to go foward.
* Press [left arrow] key to turn left.
* Press [right arrow] key to turn right.
* Press [down arrow] key to go back.


