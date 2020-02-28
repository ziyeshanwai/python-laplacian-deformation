clc;
clear all;
close all;
file_name = "./testfor_matlb_lapacian_deformation.obj";
[vertex,faces, N] = load_obj(file_name); 
BI = [2531,1232];
BC = [12.0877, 155.7108, -11.9104;3.3880, 155.6416, -5.5550];
U=laplacian_surface_editing_3D(vertex,faces,BI,BC);
write_obj_file(U, faces, N, "output.obj");