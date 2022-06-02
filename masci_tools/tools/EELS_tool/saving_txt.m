filename_write=strcat(app.NameEditField.Value,'_plot.dat');
start=['#x','y'];
dlmwrite(filename_write,start)%
for i=1:(size(energy_mesh))
    dlmwrite(filename_write,[energy_mesh(i)',dielec_plot(i)'],'delimiter','\t','-append')
end
% filename_write=strcat(app.NameEditField.Value,'_full',num2str(jsp),'.dat');
% start=['#Energy (eV)','Real','Imag'];
% dlmwrite(filename_write,start)%
% dlmwrite(filename_write,[energy_mesh(:)',dielec_plot(:)'],'-append')
