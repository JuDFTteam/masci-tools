function axout = molecule3D(varargin)
%MOLECULE3D Draw 3D molecules
%   MOLECULE3D(XYZ,LAB) draws the molecule defined by the position matrix
%   XYZ based on the labels in the cell array LAB. XYZ is a matrix with
%   three columns representing the cartesian coordinates x, y and z in
%   Ångström with one line per atom. LAB is used to adapt the color and
%   geometry of each atom. Bonds are added if the distance between two
%   atoms is closer than 1.6 Å.
%
%   MOLECULE3D(XYZ,LAB,STYLE) allows to change the appearance of the
%   molecule. STYLE can be on of the strings 'ballstick', 'licorice',
%   'large', or 'superlarge'. Just try it out!
%
%   MOLECULE3D(AX,...) plots into AX as the main axes, instead of GCA.
%
%   AX = MOLECULE3D(...) returns the handle of the axis.
%
%   Check out the examples in example_molecule3D.m!
%
%   Version: 1.2
%   Author:  André Ludwig (aludwig@phys.ethz.ch)

% geometry settings
RC = 0.2; % radius of bonds
DBOND = 2.5; % maximal distance of atoms forming bond

% resolution of spheres and cylinders
NS = 50; % spheres, more looks smoother
NB = 50; % more looks smoother

% check input arguments
narginchk(2,inf);

if numel(varargin{1}) == 1 && ishghandle(varargin{1}(1)) && ...
        isequal(lower(char(get(varargin{1}(1),'type'))),'axes')
    ax = varargin{1};
    offs = 1;
else
    ax = [];
    offs = 0;
end

xyz = varargin{1+offs};
Na = size(xyz,1); % number of atoms in molecule

lab = varargin{2+offs};
if ~iscellstr(lab)
    error('Input LAB has to be a cell string')
end
lab = lab(:); % convert to column vector

if nargin - offs < 3
    style = 'ballstick'; % set default style to rad/stick
else
    style = varargin{3+offs};
end

if ~any(strcmp(style,{'ballstick','licorice','large','superlarge'}))
    warning('Style "%s" not found.',style)
    style = 'ballstick'; % fallback
end

if size(xyz,2) ~= 3 || Na < 1
    error('First argument should be N times 3 matrix.')
end

if numel(lab) ~= Na
    error('Number of labels does not match number of columns.')
end

% prepare axis
ax = newplot(ax);
axes(ax);
set(ax,'Visible','off','DataAspectRatio',[1 1 1]) % fix aspect ratio

light('Position',[1 1 2]); % add some light

% all combinations of atom pairs
pairs = combnk(1:Na,2);
% all interatomic distances
ds = sqrt(sum((xyz(pairs(:,1),:) - xyz(pairs(:,2),:)).^2,2)); 

% find bonds based on distances of atoms
ks = find(ds < DBOND & ~(strcmp(lab(pairs(:,1)),'H') & ...
    strcmp(lab(pairs(:,2)),'H')))';

% draw sphere with adapted radius for each element / line in xyz
for k = 1:size(xyz,1)
    thiscol = col(lab{k});
    
    switch style
        case 'ballstick'
            thisr = rad(lab{k});
        case 'licorice'
            thisr = RC;
        case 'large'
            thisr = 2*rad(lab{k});
        case 'superlarge'
            thisr = 3*rad(lab{k});
    end
    
    % basic sphere
    [sx,sy,sz] = sphere(NS);
    
    % draw sphere
    surface('XData',xyz(k,1) + thisr*sx,'YData',xyz(k,2) + thisr*sy, ...
        'ZData',xyz(k,3) + thisr*sz,'FaceColor',thiscol, ...
        'EdgeColor','none','FaceLighting','gouraud')
end

% draw cylinders for each bond
for k = ks % draw sticks for all bounds
    r1 = xyz(pairs(k,1),:); % coordinates atom 1
    r2 = xyz(pairs(k,2),:); % coordinates atom 2
    
    % bond angles in spherical coordinates
    v = (r2-r1)/norm(r2-r1);
    phi = atan2d(v(2),v(1));
    theta = -asind(v(3));
    
    % bond distance minus sphere radii
    bd = ds(k) - rad(lab{pairs(k,1)}) - rad(lab{pairs(k,2)});
    cyl2 = rad(lab{pairs(k,1)}) + bd/2; % length half bond cylinder
    cyl1 = ds(k); % length full bond cylinder
    
    % prototype cylinders for bond
    [z,y,x] = cylinder(RC,NB); % full bond cylinder
    x(2,:) = x(2,:) * cyl1; % adjust length
    [z2,y2,x2] = cylinder(RC*1.01,NB); % half bond cylinder, thicker
    x2(2,:) = x2(2,:) * cyl2; % adjust length
    
    % rotate cylinders to match bond vector v
    for kk = 1:numel(x)
        vr = [x(kk); y(kk); z(kk);];
        vr = rotz(phi)*roty(theta)*vr;
        x(kk) = vr(1);
        y(kk) = vr(2);
        z(kk) = vr(3);
        
        vr = [x2(kk); y2(kk); z2(kk);];
        vr = rotz(phi)*roty(theta)*vr;
        x2(kk) = vr(1);
        y2(kk) = vr(2);
        z2(kk) = vr(3);
    end
    
    % get colors of both atoms
    thiscol1 = col(lab{pairs(k,2)});
    thiscol2 = col(lab{pairs(k,1)});
    
    % full bond color 1
    surface('XData',r1(1) + x,'YData',r1(2) + y,...
        'ZData',r1(3) + z,'FaceColor',thiscol1,...
        'EdgeColor','none','FaceLighting','gouraud')
    
    % half bond color 2
    surface('XData',r1(1) + x2,'YData',r1(2) + y2,...
        'ZData',r1(3) + z2,'FaceColor',thiscol2,...
        'EdgeColor','none','FaceLighting','gouraud')
end

if nargout > 0
    axout = ax;
end

%---------------------------------------------
% element specific CPK colors
function c = col(s)
switch s
    case  'H', c = [1 1 1];
    case  'C', c = [0.2 0.2 0.2];
    case  'O', c = [1.0 0.1 0.1];
    case  'N', c = [0.5 0.5 0.6];
    case  'I', c = [0.4 0.1 0.7];
    case  {'F','Cl'}, c = [0.2 0.9 0.2];
    case  'Br', c = [0.6 0.1 0.1];
    case  {'He','Ne','Ar','Kr','Xe'}, c = [0.2 1.0 1.0];
    case  'P', c = [1.0 0.6 0.2];
    case  'S', c = [0.9 0.9 0.2];
    case  'B', c = [1.0 0.7 0.5];
    case  {'Li','Na','K','Rb','Cs','Fr'}, c = [0.5 0.1 1.0];
    case  {'Be','Mg','Ca','Sr','Ba','Ra'}, c = [0.1 0.5 0.1];
    case  'Ti', c = [0.6 0.6 0.6];
    case  'Fe', c = [0.9 0.5 0.1];
    case  'Si', c = [0.3 0.3 0.8];
    otherwise, c = [0.9 0.5 1.0];
end

%---------------------------------------------
% element specific radii
function r = rad(s)
switch s
    case  'H', r = 0.4;
    case  'C', r = 0.5;
    case  'O', r = 0.5;
    case  'N', r = 0.5;
    case  'I', r = 0.6;
    case  'Si',r = 0.7;
    otherwise, r = 0.5;
end