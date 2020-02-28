function U = laplacian_surface_editing_3D(vertex,faces,BI,BC)

%The file is an implementation of 'Laplacian surface editing' in 3D. The
%original accompany code with this paper is in 2D. Based on this code, I
%build the 3D version. Some comments are added for better understand.

% The function compute_mesh_laplacian and compute_vertex_ring are from 
% Toolbox Graph by Gabriel Peyre which can also be found in file exchange: 
% http://uk.mathworks.com/matlabcentral/fileexchange/5355-toolbox-graph


%Inputs: vertex 
  %   vertex  #vertex by 3 list of rest domain positions
  %   faces   #faces by 3 list of triangle indices into vertex
  %   b       #b list of indices of constraint (boundary) vertices
  %   bc      #b by 3 list of constraint positions for b
  
%Output: 
  %   U       #V by dim list of new positions

% By seamanj @ NCCA on 15/02/2017

n = length(vertex);
options.symmetrize=0;
options.normalize=1;
L = compute_mesh_laplacian(vertex, faces, 'combinatorial', options );  % ¿≠∆’¿≠Àπ
disp

delta = L * vertex; %delta is the laplacian coordinates
L_prime = [   L     zeros(n) zeros(n)   % the x-part
	       zeros(n)    L     zeros(n)   % the y-part     
           zeros(n) zeros(n)    L    ]; % the z-part
neighbors = compute_vertex_ring(faces);

 for i = 1:n
     ring = [i neighbors{i}];
      V = vertex(ring,:)';
      V = [V
      ones(1,length(ring))];%Here is ones matrix, multiplying V' becomes A in formula (10). Such writing is for associating multiplication factors of v'. 
   	  %The first row of V is x part,the second row is y part, the third one is z part, the elements in last row are all ones.
        C = zeros(length(ring) * 3, 7);
   % ... Fill C in
  for r=1:length(ring)
    C(r,:) =                [V(1,r) 0 V(3,r) (-1)*V(2,r) V(4,r) 0 0];
    C(length(ring)+r,:) =   [V(2,r) (-1)*V(3,r) 0 V(1,r) 0 V(4,r) 0];
    C(2*length(ring)+r,:) = [V(3,r) V(2,r) (-1)*V(1,r) 0 0 0 V(4,r)];
  end;  
   Cinv = pinv(C);
  s =   Cinv(1,:);
  h1 =  Cinv(2,:);
  h2 =  Cinv(3,:);
  h3 =  Cinv(4,:);
 
  delta_i = delta(i,:)';
  delta_ix = delta_i(1);
  delta_iy = delta_i(2);
  delta_iz = delta_i(3);
  
   % T*delta gives us an array of coefficients  
   % T*delta*V' equals to T(V')*delta in formula (5)
  Tdelta = [delta_ix*s       + delta_iy*(-1)*h3 + delta_iz*h2
	        delta_ix*h3      + delta_iy*s       + delta_iz*(-1)*h1
            delta_ix*(-1)*h2 + delta_iy*h1      + delta_iz*s];
        
  % updating the weights in Lx_prime, Ly_prime, Lw_prime
  % Note that L_prime has already containted L. Here L_prime represents T(V')*delta - L(V') in formula(5)
  L_prime(i,[ring (ring + n) (ring + 2*n)]) = ...
      L_prime(i,[ring (ring + n) (ring + 2*n)]) + (-1)*Tdelta(1,:);
  L_prime(i+n,[ring (ring + n) (ring + 2*n)]) = ...
      L_prime(i+n,[ring (ring + n) (ring + 2*n)]) + (-1)*Tdelta(2,:);     
  L_prime(i+n*2,[ring (ring + n) (ring + 2*n)]) = ...
      L_prime(i+n*2,[ring (ring + n) (ring + 2*n)]) + (-1)*Tdelta(3,:); 
 end
   
% weight for the constraints
w=1;

% building the least-squares system matrix
A_prime = L_prime;
rhs = zeros(3*n,1);




for j=1:length(BI)
  A_prime = [A_prime
	     w*((1:(3*n))==BI(j))
	     w*((1:(3*n))==(BI(j)+n))
         w*((1:(3*n))==(BI(j)+2*n))];
  rhs = [rhs
	 w*BC(j,1)
	 w*BC(j,2)
     w*BC(j,3)];
end;

% solving for v-primes
xyz_col = A_prime\rhs;
U = [xyz_col(1:n) xyz_col((n+1):(2*n)) xyz_col((2*n+1):(3*n))];