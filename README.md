# skybox

This repository aims to create skyboxes from the cubemaps and images procedurally generated from noise using python and panda3D.
The noise images, cubemaps and cloud cover images were created using programs from [NoiseTexture](https://github.com/taKana671/NoiseTexture) and its submodule [texture_generator](https://github.com/taKana671/texture_generator).

![Image](https://github.com/user-attachments/assets/f3e1044c-570f-417f-9a9b-b13f91b984bc)

# Requirements
* Panda3D 1.10.15
  
# Environment
* Python 3.12
* Windows11

# Skybox Demo

#### Clone this repository with submodule.
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
>>>python skybox_demo_cubemap.py
```

### Skybox from display region
```
>>>python skybox_demo_displayregion.py
```

# Controls:
* Press [Esc] to quit.
* Press [up arrow] key to go foward.
* Press [left arrow] key to turn left.
* Press [right arrow] key to turn right.
* Press [down arrow] key to go back.


