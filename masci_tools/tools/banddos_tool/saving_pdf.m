%------adapt plot info/label for latex---------------
special_points_name=deblank(special_points_name);
for i=1:size(special_points_name,1)
    temp=strjoin(special_points_name(i));
    if temp=='g'
        special_points_name(i) ={'$\mathrm{\Gamma}$'};
    else
        special_points_name(i)=special_points_name(i);
    end
end
figure(99)
hold on
grid on
ylabel('$E-E_{F} (\mathrm{eV})$') % y-axis label
if (app.replaceButton.Value) || (app.compareButton.Value)
    ylabel('$E-E_{F_{KS}} (\mathrm{eV})$') % y-axis label
end
set(gca,'XTick',kpts_dist(special_points_pos))
set(gca,'XTickLabel',special_points_name)
if app.on_kpt_maxCheckBox.Value
    axis([min(kpts_dist),max(kpts_dist(app.kpt_maxEditField.Value)),app.yMinEditField.Value,app.yMaxEditField.Value])
else
    axis([min(kpts_dist),max(kpts_dist),app.yMinEditField.Value,app.yMaxEditField.Value])
end
%line([0,0],[max(kpts_dist),0])

if app.dipoleCheckBox.Value
    caxis([0 (app.yMaxEditField.Value-app.yMinEditField.Value)]);
    colormap('hot')
    for i=dipole_min:dipole_max
        for j=dipole_min:dipole_max
            colormat=abs(eigenvalues(i,:,jsp)-eigenvalues(j,:,jsp));
            element_size = 1*(dipole_mat(i,j,:)+dipole_mat(j,i,:)).^1.5+0.0001;
            scatter(kpts_dist,eigenvalues(i,:,jsp),element_size,colormat,'fill')
        end
    end
    h=colorbar;
    ylabel(h, 'transition Energy [eV]')
end
% i=dipole_min+floor((dipole_max-dipole_min)/2);
% colorrange=linspace(app.yMinEditField.Value,app.yMaxEditField.Value,10);
% colormat=0.5*[color_set(1)*abs(eigenvalues(i,:,jsp)-eigenvalues(j,:,jsp));color_set(2)*abs(eigenvalues(i,:,jsp)-eigenvalues(j,:,jsp));color_set(3)*abs(eigenvalues(i,:,jsp)-eigenvalues(j,:,jsp));];
% colormat=colormat./max(max(colormat));
% colormap(colormat')
% colorbar('Ticks',[])

if gw==1
    if jsp==2
        color_set=[0,1,1]; %CMY
    else
        color_set=[0.6,0.3,0]; %CMY
    end
else
    if jsp==2
        color_set=[1.5,0,0]; %CMY
    else
        color_set=[0.4,0.7,1]; %CMY
    end
end

if (app.backgroundCheckBox.Value)
    if app.highlightCheckBox.Value
        color_set_bg=[1,0.89,0.1]; %CMY
        select_ev=app.stateEditField.Value;
        if (app.plus1CheckBox.Value)
            select_ev=[app.stateEditField.Value,app.stateEditField.Value+1];
        end
        if (app.minus1CheckBox.Value)
            select_ev=[app.stateEditField.Value,app.stateEditField.Value-1];
        end
        if (app.plus1CheckBox.Value && app.minus1CheckBox.Value)
            select_ev=[app.stateEditField.Value-1,app.stateEditField.Value,app.stateEditField.Value+1];
        end
    else
        select_ev=1:size(eigenvalues,1);
        color_set_bg=[0.8,0.8,0.8];
    end
    for i=select_ev
        scatter(kpts_dist,eigenvalues(i,:,jsp),app.sizeEditField.Value,color_set_bg,'fill')
    end
end
if bandcharacter==0
    if atomtype~=0
        maximum=max(max(max(sum(l_charges(:,:,:,:,jsp),1))));
        atom_typ=atomtype;
        for i=1:size(eigenvalues,1)
            colormat=[color_set(1)*(1-0.5*weights(i,:,jsp));color_set(2)*(1-0.5*weights(i,:,jsp));color_set(3)*(1-0.5*weights(i,:,jsp))];
            l_char=squeeze(sum(l_charges(:,atom_typ,i,:,jsp)));
            l_char=l_char/maximum;
            scatter(kpts_dist,eigenvalues(i,:,jsp),size_dot*transpose(squeeze(weights(i,:,jsp).^def)).*l_char,transpose(colormat),'fill')
        end
    elseif atomtype==0
        maximum=max(max(sum(sum(l_charges(:,:,:,:,jsp)))));
        for i=1:size(eigenvalues,1)
            colormat=[color_set(1)*(1-0.5*weights(i,:,jsp));color_set(2)*(1-0.5*weights(i,:,jsp));color_set(3)*(1-0.5*weights(i,:,jsp))];
            %l_char=squeeze(sum(sum(l_charges(:,:,i,:,jsp))));
            %l_char=l_char/maximum;
            %scatter(kpts_dist,eigenvalues(i,:,jsp),36*transpose(squeeze(weights(i,:,jsp))).*l_char,transpose(colormat),'fill')
            if app.SOCCheckBox.Value
                l_char=squeeze(sum(sum(l_charges(:,:,i,:,jsp))));
                l_char=l_char/maximum;
                scatter(kpts_dist,eigenvalues(i,:,jsp),size_dot*transpose(squeeze(weights(i,:,jsp).^def)).*l_char,transpose(colormat),'fill')            
            else
                scatter(kpts_dist,eigenvalues(i,:,jsp),size_dot*transpose(squeeze(weights(i,:,jsp).^def)),transpose(colormat),'fill')            
            end
        end        
    end
elseif atomtype==0
    if bandcharacter~=0
        maximum=max(max(max(sum(l_charges(:,:,:,:,jsp),2))));
        bandchar=bandcharacter; %1=s(0),2=p(1);3=d(2);4=f(3)
        for i=1:size(eigenvalues,1)
            colormat=[color_set(1)*(1-0.5*weights(i,:,jsp));color_set(2)*(1-0.5*weights(i,:,jsp));color_set(3)*(1-0.5*weights(i,:,jsp))];
            l_char=squeeze(sum(l_charges(bandchar,:,i,:,jsp)));
            l_char=l_char/maximum;
            scatter(kpts_dist,eigenvalues(i,:,jsp),size_dot*transpose(squeeze(weights(i,:,jsp).^def)).*l_char,transpose(colormat),'fill')
        end
    end
else
    maximum=max(max(max(max(l_charges))));
    bandchar=bandcharacter; %1=s(0),2=p(1);3=d(2);4=f(3)
    atom_typ=atomtype;
    for i=1:size(eigenvalues,1)
        colormat=[color_set(1)*(1-0.5*weights(i,:,jsp));color_set(2)*(1-0.5*weights(i,:,jsp));color_set(3)*(1-0.5*weights(i,:,jsp))];
        l_char=squeeze(l_charges(bandchar,atom_typ,i,:,jsp));
        l_char=l_char./maximum;
        scatter(kpts_dist,eigenvalues(i,:,jsp),size_dot*transpose(squeeze(weights(i,:,jsp).^def)).*l_char,transpose(colormat),'fill')
    end
end
if app.compareCheckBox.Value
    eigenvalues_2=h5read(app.FilenamecompareEditField.Value,'/Local/BS/eigenvalues'); %eig;kpt;jsp
    kpts_2=h5read(app.FilenamecompareEditField.Value,'/kpts/coordinates');
    b_mat_2=h5read(app.FilenamecompareEditField.Value,'/cell/reciprocalCell');
    fermi_2=h5readatt(app.FilenamecompareEditField.Value,'/general','lastFermiEnergy');
    weights_2=ones(size(eigenvalues_2));
    for i=1:size(kpts_2,2)
        kpts_2(1:3,i)=b_mat_2'*kpts_2(1:3,i);
    end
    kpts_dist_2=zeros(1,size(kpts_2,2));
    kpts_dist_2(1)=0;
    for i=2:size(kpts_2,2)
        kpts_dist_2(i)=kpts_dist_2(i-1)+sqrt((kpts_2(:,i)-kpts_2(:,i-1))'*(kpts_2(:,i)-kpts_2(:,i-1)));
    end
    eigenvalues_2=(eigenvalues_2-fermi_2)*27.2;
    color_set=[1.5,0,0];
    for i=1:size(eigenvalues_2,1)
        colormat=[color_set(1)*(1-0.5*weights_2(i,:,jsp));color_set(2)*(1-0.5*weights_2(i,:,jsp));color_set(3)*(1-0.5*weights_2(i,:,jsp))];
        scatter(kpts_dist_2,eigenvalues_2(i,:,jsp),app.pointsizecompareEditField.Value*transpose(squeeze(weights_2(i,:,jsp).^def)),transpose(colormat),'fill')
    end
end
hold off
