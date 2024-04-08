# TextTo3DScene 

TextTo3DScene generates textured 3D meshes from a given text prompt using 2D text-to-image models, specifcally of 
rooms.

This project builds off the `text2room` [project](https://github.com/lukasHoel/text2room).


## Prepare Environment

Create a conda environment:

_Note: we need to delete/ unset PYTHONHOME in order for miniconda to work_

```
conda create -n text2room python=3.9
conda activate text2room
pip install -r requirements.txt
```

Then install Pytorch3D by following the [official instructions](https://github.com/facebookresearch/pytorch3d/blob/main/INSTALL.md).
For example, to install Pytorch3D on Linux (tested with PyTorch 1.13.1, CUDA 11.7, Pytorch3D 0.7.2):

```
conda install -c fvcore -c iopath -c conda-forge fvcore iopath
pip install "git+https://github.com/facebookresearch/pytorch3d.git@stable"
```

Download the pretrained model weights for the fixed depth inpainting model, that we use:

- refer to the [official IronDepth implemention](https://github.com/baegwangbin/IronDepth) to download the files ```normal_scannet.pt``` and ```irondepth_scannet.pt```.
- place the files under ```text2room/checkpoints```


## Usage 

You will need an API key, which can be placed in `keys.py` and set to a variable named `OPENAI_API_KEY`. 

Run `python generate_scene.py`

The mesh output will be saved to the `output/` directory along with other artifacts. We care about the `.ply` file 
that ends with `quadric`. 



# Text2Room
Text2Room generates textured 3D meshes from a given text prompt using 2D text-to-image models.

This is the official repository that contains source code for the ICCV 2023 paper [Text2Room](https://lukashoel.github.io/text-to-room/).

[[arXiv](https://arxiv.org/abs/2303.11989)] [[Project Page](https://lukashoel.github.io/text-to-room/)] [[Video](https://youtu.be/fjRnFL91EZc)]

![Teaser](docs/teaser.jpg "Text2Room")

If you find Text2Room useful for your work please cite:
```
@InProceedings{hoellein2023text2room,
    author    = {H\"ollein, Lukas and Cao, Ang and Owens, Andrew and Johnson, Justin and Nie{\ss}ner, Matthias},
    title     = {Text2Room: Extracting Textured 3D Meshes from 2D Text-to-Image Models},
    booktitle = {Proceedings of the IEEE/CVF International Conference on Computer Vision (ICCV)},
    month     = {October},
    year      = {2023},
    pages     = {7909-7920}
}
```

## Prepare Environment

Create a conda environment:

_Note: we need to delete/ unset PYTHONHOME in order for miniconda to work_

```
conda create -n text2room python=3.9
conda activate text2room
pip install -r requirements.txt
```

Then install Pytorch3D by following the [official instructions](https://github.com/facebookresearch/pytorch3d/blob/main/INSTALL.md).
For example, to install Pytorch3D on Linux (tested with PyTorch 1.13.1, CUDA 11.7, Pytorch3D 0.7.2):

```
conda install -c fvcore -c iopath -c conda-forge fvcore iopath
pip install "git+https://github.com/facebookresearch/pytorch3d.git@stable"
```

Download the pretrained model weights for the fixed depth inpainting model, that we use:

- refer to the [official IronDepth implemention](https://github.com/baegwangbin/IronDepth) to download the files ```normal_scannet.pt``` and ```irondepth_scannet.pt```.
- place the files under ```text2room/checkpoints```

(Optional) Download the pretrained model weights for the text-to-image model:

- ```git clone https://huggingface.co/stabilityai/stable-diffusion-2-inpainting```
- ```git clone https://huggingface.co/stabilityai/stable-diffusion-2-1```
- ```ln -s <path/to/stable-diffusion-2-inpainting> checkpoints```
- ```ln -s <path/to/stable-diffusion-2-1> checkpoints```

## Generate a Scene

As default, we generate a living room scene:

```python generate_scene.py```

Outputs are stored in ```text2room/output```.

See the `text2room` repo for more instructions on customizing the mesh generation. 

## Notes on our implementation 

Empirically we found the best results by... (explain how we attenuated the text2room pipeline)