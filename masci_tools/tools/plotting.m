if jsp==2
    color_set=[1.5,0,0]; %CMY
else
    color_set=[0.4,0.7,1]; %CMY
end
if (app.backgroundCheckBox.Value)
    for i=1:size(eigenvalues,1)
        scatter(app.UIAxes,kpts_dist,eigenvalues(i,:,jsp),0.1*size_dot,[0.8,0.8,0.8],'fill')
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
        %maximum=max(max(sum(sum(l_charges(:,:,:,:,jsp)))));
        for i=1:size(eigenvalues,1)
            colormat=[color_set(1)*(1-0.5*weights(i,:,jsp));color_set(2)*(1-0.5*weights(i,:,jsp));color_set(3)*(1-0.5*weights(i,:,jsp))];
            %l_char=squeeze(sum(sum(l_charges(:,:,i,:,jsp))));
            %l_char=l_char/maximum;
            %scatter(kpts_dist,eigenvalues(i,:,jsp),36*transpose(squeeze(weights(i,:,jsp))).*l_char,transpose(colormat),'fill')
            scatter(app.UIAxes,kpts_dist,eigenvalues(i,:,jsp),size_dot*transpose(squeeze(weights(i,:,jsp).^def)),transpose(colormat),'fill')
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
hold(app.UIAxes,'off')