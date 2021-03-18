# Computer Graphics

## Projection

This script takes two pictures: the texture and the scene.
- The texture is an image which one wishes to project.
- The scene is a 3D image in which one wishes to project the texture.

Usage:
`projection.py <texture_path> <scene_path>`

The user is able to choose the coordinates of both the texture's and the scene's quadrilateral. 

Here's an example and its output:

```
> projection.py images/nutella.jpg images/art-museum.jpg

Do you want to project the whole texture onto the scene? (y/n)
y
Enter the coordinates of the scene quadrilateral vertices.
Upper left vertex
X: 54
Y: 161
Upper right vertex
X: 154
Y: 172
Bottom left vertex
X: 53
Y: 310
Bottom right vertex
X: 152
Y: 299
```

![resulting image](images/result.jpg)
