figure(99)
hold on
grid on
xlabel('Energy $(\mathrm{eV})$') % x-axis label
if (app.typeDropDown.Value=='3') %EELS
    ylabel('EELS') % y-axis label
elseif (app.typeDropDown.Value=='2') %real(eps)
    ylabel('$\Re(\varepsilon)$') % y-axis label
elseif (app.typeDropDown.Value=='1') %imag(eps)
    ylabel('$\Im(\varepsilon)$') % y-axis label
end
axis([app.xMinEditField.Value,app.xMaxEditField.Value,app.yMinEditField.Value,app.yMaxEditField.Value])
plot(energy_mesh(:),dielec_plot(:))
if app.experimtaldataCheckBox.Value
hold on
plot(exp_data(:,1)+app.shiftEditField.Value,(exp_data(:,2)-app.offsetEditField.Value)*app.scaleEditField.Value)
end
if app.holdCheckBox.Value
    hold on
else
    hold off
end

figure(98)
hold on
grid on
xlabel('reciprocal space [$1/\text{Angstrom}$]') % x-axis label
ylabel('reciprocal space [$1/\text{Angstrom}$]') % y-axis label
axis([0,max(q_array(:,4))^(1/2)/0.529,0,max(q_array(:,4))^(1/2)/0.529])
color_set=[0.8,0.2,0];
scatter(q_array(:,1)/0.529,q_array(:,2)/0.529,5,color_set,'fill')
if app.useadditionalkptssetCheckBox.Value
    color_set=[0.2,0.8,0];
    scatter(q_array_2(:,1)/0.529,q_array_2(:,2)/0.529,5,color_set,'fill')
end
hold off

% %------adapt plot info/label for latex---------------
% special_points_name=deblank(special_points_name);
% for i=1:size(special_points_name,1)
%     temp=strjoin(special_points_name(i));
%     if temp=='g'
%         special_points_name(i) ={'$\mathrm{\Gamma}$'};
%     else
%         special_points_name(i)=special_points_name(i);
%     end
% end
% figure(99)
% hold on
% grid on
% ylabel('$E-E_{F} (\mathrm{eV})$') % y-axis label
% if (app.replaceButton.Value) || (app.compareButton.Value)
%     ylabel('$E-E_{F_{KS}} (\mathrm{eV})$') % y-axis label
% end
% set(gca,'XTick',kpts_dist(special_points_pos))
% set(gca,'XTickLabel',special_points_name)
% axis([min(kpts_dist),max(kpts_dist),app.yMinEditField.Value,app.yMaxEditField.Value])
% %line([0,0],[max(kpts_dist),0])
% if gw==1
%     if jsp==2
%         color_set=[0,1,1]; %CMY
%     else
%         color_set=[0.6,0.3,0]; %CMY
%     end
% else
%     if jsp==2
%         color_set=[1.5,0,0]; %CMY
%     else
%         color_set=[0.4,0.7,1]; %CMY
%     end
% end
% if (app.backgroundCheckBox.Value)
%     if app.highlightCheckBox.Value
%         color_set_bg=[1,0.89,0.1]; %CMY
%         select_ev=app.stateEditField.Value;
%         if (app.plus1CheckBox.Value)
%             select_ev=[app.stateEditField.Value,app.stateEditField.Value+1];
%         end
%         if (app.minus1CheckBox.Value)
%             select_ev=[app.stateEditField.Value,app.stateEditField.Value-1];
%         end
%         if (app.plus1CheckBox.Value && app.minus1CheckBox.Value)
%             select_ev=[app.stateEditField.Value-1,app.stateEditField.Value,app.stateEditField.Value+1];
%         end
%     else
%         select_ev=1:size(eigenvalues,1);
%         color_set_bg=[0.8,0.8,0.8];
%     end
%     for i=select_ev
%         scatter(kpts_dist,eigenvalues(i,:,jsp),app.sizeEditField.Value,color_set_bg,'fill')
%     end
% end
% if bandcharacter==0
%     if atomtype~=0
%         maximum=max(max(max(sum(l_charges(:,:,:,:,jsp),1))));
%         atom_typ=atomtype;
%         for i=1:size(eigenvalues,1)
%             colormat=[color_set(1)*(1-0.5*weights(i,:,jsp));color_set(2)*(1-0.5*weights(i,:,jsp));color_set(3)*(1-0.5*weights(i,:,jsp))];
%             l_char=squeeze(sum(l_charges(:,atom_typ,i,:,jsp)));
%             l_char=l_char/maximum;
%             scatter(kpts_dist,eigenvalues(i,:,jsp),size_dot*transpose(squeeze(weights(i,:,jsp).^def)).*l_char,transpose(colormat),'fill')
%         end
%     elseif atomtype==0
%         maximum=max(max(sum(sum(l_charges(:,:,:,:,jsp)))));
%         for i=1:size(eigenvalues,1)
%             colormat=[color_set(1)*(1-0.5*weights(i,:,jsp));color_set(2)*(1-0.5*weights(i,:,jsp));color_set(3)*(1-0.5*weights(i,:,jsp))];
%             %l_char=squeeze(sum(sum(l_charges(:,:,i,:,jsp))));
%             %l_char=l_char/maximum;
%             %scatter(kpts_dist,eigenvalues(i,:,jsp),36*transpose(squeeze(weights(i,:,jsp))).*l_char,transpose(colormat),'fill')
%             if app.SOCCheckBox.Value
%                 l_char=squeeze(sum(sum(l_charges(:,:,i,:,jsp))));
%                 l_char=l_char/maximum;
%                 scatter(kpts_dist,eigenvalues(i,:,jsp),size_dot*transpose(squeeze(weights(i,:,jsp).^def)).*l_char,transpose(colormat),'fill')
%             else
%                 scatter(kpts_dist,eigenvalues(i,:,jsp),size_dot*transpose(squeeze(weights(i,:,jsp).^def)),transpose(colormat),'fill')
%             end
%         end
%     end
% elseif atomtype==0
%     if bandcharacter~=0
%         maximum=max(max(max(sum(l_charges(:,:,:,:,jsp),2))));
%         bandchar=bandcharacter; %1=s(0),2=p(1);3=d(2);4=f(3)
%         for i=1:size(eigenvalues,1)
%             colormat=[color_set(1)*(1-0.5*weights(i,:,jsp));color_set(2)*(1-0.5*weights(i,:,jsp));color_set(3)*(1-0.5*weights(i,:,jsp))];
%             l_char=squeeze(sum(l_charges(bandchar,:,i,:,jsp)));
%             l_char=l_char/maximum;
%             scatter(kpts_dist,eigenvalues(i,:,jsp),size_dot*transpose(squeeze(weights(i,:,jsp).^def)).*l_char,transpose(colormat),'fill')
%         end
%     end
% else
%     maximum=max(max(max(max(l_charges))));
%     bandchar=bandcharacter; %1=s(0),2=p(1);3=d(2);4=f(3)
%     atom_typ=atomtype;
%     for i=1:size(eigenvalues,1)
%         colormat=[color_set(1)*(1-0.5*weights(i,:,jsp));color_set(2)*(1-0.5*weights(i,:,jsp));color_set(3)*(1-0.5*weights(i,:,jsp))];
%         l_char=squeeze(l_charges(bandchar,atom_typ,i,:,jsp));
%         l_char=l_char./maximum;
%         scatter(kpts_dist,eigenvalues(i,:,jsp),size_dot*transpose(squeeze(weights(i,:,jsp).^def)).*l_char,transpose(colormat),'fill')
%     end
% end
% hold off
