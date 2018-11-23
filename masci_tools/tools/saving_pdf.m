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
set(gca,'XTick',kpts_dist(special_points_pos))
set(gca,'XTickLabel',special_points_name)
axis([min(kpts_dist),max(kpts_dist),app.yMinEditField.Value,app.yMaxEditField.Value])
%line([0,0],[max(kpts_dist),0])
if jsp==2
    color_set=[1.5,0,0]; %CMY
else
    color_set=[0.4,0.7,1]; %CMY
end
if (app.backgroundCheckBox.Value)
    for i=1:size(eigenvalues,1)
        scatter(kpts_dist,eigenvalues(i,:,jsp),0.1*size_dot,[0.8,0.8,0.8],'fill')
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
        %maximum=max(max(sum(sum(l_charges(:,:,:,:,jsp)))));
        for i=1:size(eigenvalues,1)
            colormat=[color_set(1)*(1-0.5*weights(i,:,jsp));color_set(2)*(1-0.5*weights(i,:,jsp));color_set(3)*(1-0.5*weights(i,:,jsp))];
            %l_char=squeeze(sum(sum(l_charges(:,:,i,:,jsp))));
            %l_char=l_char/maximum;
            %scatter(kpts_dist,eigenvalues(i,:,jsp),36*transpose(squeeze(weights(i,:,jsp))).*l_char,transpose(colormat),'fill')
            scatter(kpts_dist,eigenvalues(i,:,jsp),size_dot*transpose(squeeze(weights(i,:,jsp).^def)),transpose(colormat),'fill')
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
        l_char=l_char/maximum;
        scatter(kpts_dist,eigenvalues(i,:,jsp),size_dot*transpose(squeeze(weights(i,:,jsp).^def)).*l_char,transpose(colormat),'fill')
    end
end
hold off