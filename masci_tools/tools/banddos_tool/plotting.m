if app.dipoleCheckBox.Value
    color_set=[0.6,0.3,0]; %CMY
    for i=dipole_min:dipole_max
        for j=dipole_min:dipole_max
            colormat=0.5*[color_set(1)*abs(eigenvalues(i,:,jsp)-eigenvalues(j,:,jsp));color_set(2)*abs(eigenvalues(i,:,jsp)-eigenvalues(j,:,jsp));color_set(3)*abs(eigenvalues(i,:,jsp)-eigenvalues(j,:,jsp));];
            element_size =  1*(dipole_mat(i,j,:)+dipole_mat(j,i,:)).^1.5+0.0001;
            scatter(app.UIAxes,kpts_dist,eigenvalues(i,:,jsp),element_size,transpose(colormat),'fill')
        end
    end
end
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
    for i=select_ev;
        scatter(app.UIAxes,kpts_dist,eigenvalues(i,:,jsp),app.sizeEditField.Value,color_set_bg,'fill')
    end
end
if bandcharacter==0
    if atomtype~=0
        maximum=max(max(max(sum(l_charges(:,:,:,:,jsp),1))));
        atom_typ=atomtype;
        for i=1:size(eigenvalues,1)
            %colormat=[1-weights(i,:,jsp);0.8*ones(1,size(weights(i,:,jsp),2));0.8*ones(1,size(weights(i,:,jsp),2))];
            colormat=[color_set(1)*(1-0.5*weights(i,:,jsp));color_set(2)*(1-0.5*weights(i,:,jsp));color_set(3)*(1-0.5*weights(i,:,jsp))];
            l_char=squeeze(sum(l_charges(:,atom_typ,i,:,jsp)));
            l_char=l_char/maximum;
            scatter(app.UIAxes,kpts_dist,eigenvalues(i,:,jsp),size_dot*transpose(squeeze(weights(i,:,jsp).^def)).*l_char,transpose(colormat),'fill')
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
                scatter(app.UIAxes,kpts_dist,eigenvalues(i,:,jsp),size_dot*transpose(squeeze(weights(i,:,jsp).^def)).*l_char,transpose(colormat),'fill')
            else
                scatter(app.UIAxes,kpts_dist,eigenvalues(i,:,jsp),size_dot*transpose(squeeze(weights(i,:,jsp).^def)),transpose(colormat),'fill')
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
            scatter(app.UIAxes,kpts_dist,eigenvalues(i,:,jsp),size_dot*transpose(squeeze(weights(i,:,jsp).^def)).*l_char,transpose(colormat),'fill')
        end
    end
else
    maximum=max(max(max(max(l_charges(:,:,:,:,jsp)))));
    bandchar=bandcharacter; %1=s(0),2=p(1);3=d(2);4=f(3)
    atom_typ=atomtype;
    for i=1:size(eigenvalues,1)
        colormat=[color_set(1)*(1-0.5*weights(i,:,jsp));color_set(2)*(1-0.5*weights(i,:,jsp));color_set(3)*(1-0.5*weights(i,:,jsp))];
        l_char=squeeze(l_charges(bandchar,atom_typ,i,:,jsp));
        l_char=l_char/maximum;
        scatter(app.UIAxes,kpts_dist,eigenvalues(i,:,jsp),size_dot*transpose(squeeze(weights(i,:,jsp).^def)).*l_char,transpose(colormat),'fill')
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
        scatter(app.UIAxes,kpts_dist_2,eigenvalues_2(i,:,jsp),app.pointsizecompareEditField.Value*transpose(squeeze(weights_2(i,:,jsp).^def)),transpose(colormat),'fill')
    end
end
hold(app.UIAxes,'off')
