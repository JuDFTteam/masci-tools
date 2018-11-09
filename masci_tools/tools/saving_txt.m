if app.saveplotdataCheckBox.Value
    filename_write=strcat(app.NameEditField.Value,'_',num2str(jsp),'.dat');
    start=['#x','y','w'];
    for i=1:size(special_points_name,1)
        special_points_name_str(i)=strjoin(deblank(special_points_name(i)));
    end
    dlmwrite(filename_write,start)
    dlmwrite(strcat(app.NameEditField.Value,'_special_kpts.dat'),special_points_name_str)
    dlmwrite(strcat(app.NameEditField.Value,'_special_kpts.dat'),kpts_dist(special_points_pos),'-append')
    
    if bandcharacter==0
        if atomtype~=0
            maximum=max(max(max(sum(l_charges(:,:,:,:,jsp),1))));
            atom_typ=atomtype;
            for i=1:size(eigenvalues,1)
                l_char=squeeze(sum(l_charges(:,atom_typ,i,:,jsp)));
                l_char=l_char/maximum;
                dlmwrite(filename_write,[kpts_dist',eigenvalues(i,:,jsp)',transpose(squeeze(weights(i,:,jsp).^def)).*l_char],'-append')
            end
        elseif atomtype==0
            for i=1:size(eigenvalues,1)
                dlmwrite(filename_write,[kpts_dist',eigenvalues(i,:,jsp)',transpose(squeeze(weights(i,:,jsp).^def))],'-append')
            end
        end
    elseif atomtype==0
        if bandcharacter~=0
            maximum=max(max(max(sum(l_charges(:,:,:,:,jsp),2))));
            bandchar=bandcharacter; %1=s(0),2=p(1);3=d(2);4=f(3)
            for i=1:size(eigenvalues,1)
                l_char=squeeze(sum(l_charges(bandchar,:,i,:,jsp)));
                l_char=l_char/maximum;
                dlmwrite(filename_write,[kpts_dist',eigenvalues(i,:,jsp)',transpose(squeeze(weights(i,:,jsp).^def)).*l_char],'-append')
            end
        end
    else
        maximum=max(max(max(max(l_charges))));
        bandchar=bandcharacter; %1=s(0),2=p(1);3=d(2);4=f(3)
        atom_typ=atomtype;
        for i=1:size(eigenvalues,1)
            l_char=squeeze(l_charges(bandchar,atom_typ,i,:,jsp));
            l_char=l_char/maximum;
            dlmwrite(filename_write,[kpts_dist',eigenvalues(i,:,jsp)',transpose(squeeze(weights(i,:,jsp).^def)).*l_char],'-append')
        end
    end
end