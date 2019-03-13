 
classdef banddos_analysis_1 < matlab.apps.AppBase

    % Properties that correspond to app components
    properties (Access = public)
        UIFigure                       matlab.ui.Figure
        UIAxes                         matlab.ui.control.UIAxes
        bandcharacterButtonGroup       matlab.ui.container.ButtonGroup
        sButton                        matlab.ui.control.RadioButton
        pButton                        matlab.ui.control.RadioButton
        dButton                        matlab.ui.control.RadioButton
        fButton                        matlab.ui.control.RadioButton
        allButton                      matlab.ui.control.RadioButton
        updateButton                   matlab.ui.control.Button
        UIAxes2                        matlab.ui.control.UIAxes
        FilenameEditFieldLabel         matlab.ui.control.Label
        FilenameEditField              matlab.ui.control.EditField
        unfoldbandstrCheckBox          matlab.ui.control.CheckBox
        atomgroupDropDownLabel         matlab.ui.control.Label
        atomgroupDropDown              matlab.ui.control.DropDown
        plotatomicstructureButton      matlab.ui.control.Button
        savePDFCheckBox                matlab.ui.control.CheckBox
        saveplotdataCheckBox           matlab.ui.control.CheckBox
        NameEditFieldLabel             matlab.ui.control.Label
        NameEditField                  matlab.ui.control.EditField
        yMinEditFieldLabel             matlab.ui.control.Label
        yMinEditField                  matlab.ui.control.NumericEditField
        yMaxEditFieldLabel             matlab.ui.control.Label
        yMaxEditField                  matlab.ui.control.NumericEditField
        jspDropDownLabel               matlab.ui.control.Label
        jspDropDown                    matlab.ui.control.DropDown
        UnfoldingIntensitySliderLabel  matlab.ui.control.Label
        UnfoldingIntensitySlider       matlab.ui.control.Slider
        backgroundCheckBox             matlab.ui.control.CheckBox
        pointsizeEditFieldLabel        matlab.ui.control.Label
        pointsizeEditField             matlab.ui.control.NumericEditField
    end

    methods (Access = public)
        
    end
    

    methods (Access = private)

        % Button pushed function: updateButton
        function updateButtonPushed(app, event)
            app.UIAxes.cla; %clear graph
            close all
            if app.FilenameEditField.Value=="" %fallback when no input file is given
                app.FilenameEditField.Value='banddos.hdf';
            end
            filename_l=app.FilenameEditField.Value;
            filename=app.FilenameEditField.Value;
            %------------------reading hdf5file values-----------------
            a_mat =h5read(filename,'/cell/bravaisMatrix');
            b_mat =h5read(filename,'/cell/reciprocalCell');            
            bohr_const=0.52;
            a_mat=a_mat*bohr_const;
            atoms =h5read(filename,'/atoms/positions');
            for i=1:size(atoms,2)
                atoms(1:3,i)=a_mat*atoms(1:3,i);
            end
            atoms(4,:)=h5read(filename,'/atoms/atomicNumbers');
            atoms(5,:)=h5read(filename,'/atoms/equivAtomsGroup');
            special_points_name =h5read(filename_l,'/kpts/specialPointLabels');
            %special_points_name ={'g'};
            special_points_pos =h5read(filename_l,'/kpts/specialPointIndices');
            %special_points_pos =[1];
            kpts=h5read(filename,'/kpts/coordinates');
            for i=1:size(kpts,2)
               kpts(1:3,i)=b_mat*kpts(1:3,i);
            end
            kpts_dist=zeros(1,size(kpts,2));
            kpts_dist(1)=0;
            for i=2:size(kpts,2)
                kpts_dist(i)=kpts_dist(i-1)+sqrt((kpts(:,i)-kpts(:,i-1))'*(kpts(:,i)-kpts(:,i-1)));
            end
            eigenvalues=h5read(filename,'/eigenvalues/eigenvalues'); %eig;kpt;jsp
            if (app.unfoldbandstrCheckBox.Value)
                weights=h5read(filename,'/bandUnfolding/weights'); %eig;kpt;jsp
                for i=1:size(weights,1)
                    for j=1:size(weights,2)
                        if weights(i,j)==0
                            weights(i,j)=0.00000000001;
                        end
                    end
                end
            else
                weights=ones(size(eigenvalues));
            end
            l_charges=h5read(filename,'/eigenvalues/lLikeCharge'); %l_character[0,1,2,3];atoms_ntype;eig;kpt;jsp
            fermi=h5readatt(filename,'/general','lastFermiEnergy');
            eigenvalues=(eigenvalues-fermi)*27.2;
            %--------------atomtype selection-------------------------------
            atomtype_list(1)={'all'};
            atomtype_numlist=min(atoms(5,:)):max(atoms(5,:));
            atomtype_numlist=squeeze(atomtype_numlist);
            for i=1:(size(atomtype_numlist,2))
                atomtype_list(i+1)={num2str(atomtype_numlist(i))};
            end
            atomtype_numlist=[0,atomtype_numlist];
            app.atomgroupDropDown.Items = atomtype_list;
            app.atomgroupDropDown.ItemsData = atomtype_numlist;
            atomtype=app.atomgroupDropDown.Value;          %0 means all
            %------------ jsp selection----------
            if size(eigenvalues,3)==2
                app.jspDropDown.Items = [{'both'},{'1'},{'2'}];
                app.jspDropDown.ItemsData = [0,1,2];
            else
                app.jspDropDown.Items = {'1'};
                app.jspDropDown.ItemsData = 1;
            end
            jsp=app.jspDropDown.Value; %spin
            %---------------------bandcharacter selection----------------
            if app.sButton.Value
                bandcharacter=1; %0 means all
            end
            if app.pButton.Value
                bandcharacter=2; %0 means all
            end
            if app.dButton.Value
                bandcharacter=3; %0 means all
            end
            if app.fButton.Value
                bandcharacter=4; %0 means all
            end
            if app.allButton.Value
                bandcharacter=0; %0 means all
            end
            %---------------------output name default----------------
            if app.NameEditField.Value==""
                app.NameEditField.Value='bandstructure';
            end
            %---------------------defect intensity----------------------
            def=app.UnfoldingIntensitySlider.Value;
            %---------------------setting graph properties---------------
            hold(app.UIAxes,'on')
            ylabel(app.UIAxes,'E-E_F (eV)') % y-axis label
            xlabel(app.UIAxes,'')    % x-axis label
            app.UIAxes.XTick = kpts_dist(special_points_pos);
            %app.UIAxes.GridColor = [0.15 0.15 0.15];
            %app.UIAxes.MinorGridColor = [0.1 0.1 0.1];
            app.UIAxes.XTickLabel = deblank(special_points_name);
            if app.yMinEditField.Value==0
                app.yMinEditField.Value=min(min(min(eigenvalues)));
            end
            if app.yMaxEditField.Value==0
                app.yMaxEditField.Value=max(max(max(eigenvalues)));
            end
            axis(app.UIAxes,[min(kpts_dist),max(kpts_dist),app.yMinEditField.Value,app.yMaxEditField.Value])
            %color_set=[0.4,0.7,1]; %CMY
            size_dot=app.pointsizeEditField.Value;
            %----------------------plotting-----------------------------
            if jsp==0
                jsp=1;
                plotting
                hold(app.UIAxes,'on')
                if app.savePDFCheckBox.Value
                    saving_pdf
                    hold on
                end
                saving_txt
                jsp=2;
                plotting
                if app.savePDFCheckBox.Value
                    saving_pdf
                    matlabfrag(app.NameEditField.Value);
                    mlf2pdf(99,app.NameEditField.Value);
                end
                saving_txt
            else
                plotting
                if app.savePDFCheckBox.Value
                    saving_pdf
                    matlabfrag(app.NameEditField.Value);
                    mlf2pdf(99,app.NameEditField.Value);
                end
                saving_txt
            end
            %--------plot atom groups----------
            colorbar(app.UIAxes2)
            colormap(app.UIAxes2, 'jet' )
            zlabel(app.UIAxes2,'')
            scatter3(app.UIAxes2,atoms(1,:),atoms(2,:),atoms(3,:),40*atoms(4,:),atoms(5,:),'fill')
        end

        % Button pushed function: plotatomicstructureButton
        function plotatomicstructureButtonPushed(app, event)
            filename=app.FilenameEditField.Value;
            a_mat =h5read(filename,'/cell/bravaisMatrix');
            bohr_const=0.52;
            a_mat=a_mat*bohr_const;
            atoms =h5read(filename,'/atoms/positions');
            for i=1:size(atoms,2)
                atoms(1:3,i)=a_mat*atoms(1:3,i);
            end
            atoms(4,:)=h5read(filename,'/atoms/atomicNumbers');
            atoms(5,:)=h5read(filename,'/atoms/equivAtomsGroup');
            
            for i=1:size(atoms,2)
                xyz(i,1:3)=atoms(1:3,i);
                if atoms(4,i)==14
                    labels(i) ={'Si'};
                elseif atoms(4,i)==6
                    labels(i) ={'C'};
                else
                    labels(i)={'Unknown'};
                end
            end
            figure(10)
            set(gcf,'Color','w')
            molecule3D(xyz,labels,'ballstick')
        end
    end

    % App initialization and construction
    methods (Access = private)

        % Create UIFigure and components
        function createComponents(app)

            % Create UIFigure
            app.UIFigure = uifigure;
            app.UIFigure.Position = [100 100 640 480];
            app.UIFigure.Name = 'UI Figure';

            % Create UIAxes
            app.UIAxes = uiaxes(app.UIFigure);
            title(app.UIAxes, 'electronic band structure')
            app.UIAxes.PlotBoxAspectRatio = [1 0.500717360114778 0.500717360114778];
            app.UIAxes.YGrid = 'on';
            app.UIAxes.Position = [11 14 450 255];

            % Create bandcharacterButtonGroup
            app.bandcharacterButtonGroup = uibuttongroup(app.UIFigure);
            app.bandcharacterButtonGroup.Title = 'band character';
            app.bandcharacterButtonGroup.Position = [491 280 100 129];

            % Create sButton
            app.sButton = uiradiobutton(app.bandcharacterButtonGroup);
            app.sButton.Text = 's';
            app.sButton.Position = [11 83 58 22];

            % Create pButton
            app.pButton = uiradiobutton(app.bandcharacterButtonGroup);
            app.pButton.Text = 'p';
            app.pButton.Position = [11 61 65 22];

            % Create dButton
            app.dButton = uiradiobutton(app.bandcharacterButtonGroup);
            app.dButton.Text = 'd';
            app.dButton.Position = [11 39 65 22];

            % Create fButton
            app.fButton = uiradiobutton(app.bandcharacterButtonGroup);
            app.fButton.Text = 'f';
            app.fButton.Position = [11 18 26 22];

            % Create allButton
            app.allButton = uiradiobutton(app.bandcharacterButtonGroup);
            app.allButton.Text = 'all';
            app.allButton.Position = [11 1 34 22];
            app.allButton.Value = true;

            % Create updateButton
            app.updateButton = uibutton(app.UIFigure, 'push');
            app.updateButton.ButtonPushedFcn = createCallbackFcn(app, @updateButtonPushed, true);
            app.updateButton.Position = [491 34 100 22];
            app.updateButton.Text = 'update';

            % Create UIAxes2
            app.UIAxes2 = uiaxes(app.UIFigure);
            title(app.UIAxes2, 'atom groups')
            app.UIAxes2.PlotBoxAspectRatio = [1 0.512471655328798 0.512471655328798];
            app.UIAxes2.Box = 'on';
            app.UIAxes2.XTick = [];
            app.UIAxes2.YTick = [];
            app.UIAxes2.XGrid = 'on';
            app.UIAxes2.XMinorGrid = 'on';
            app.UIAxes2.YGrid = 'on';
            app.UIAxes2.YMinorGrid = 'on';
            app.UIAxes2.ZGrid = 'on';
            app.UIAxes2.ZMinorGrid = 'on';
            app.UIAxes2.BackgroundColor = [0.9412 0.9412 0.9412];
            app.UIAxes2.Position = [24 268 267 165];

            % Create FilenameEditFieldLabel
            app.FilenameEditFieldLabel = uilabel(app.UIFigure);
            app.FilenameEditFieldLabel.HorizontalAlignment = 'right';
            app.FilenameEditFieldLabel.Position = [24 442 55 22];
            app.FilenameEditFieldLabel.Text = 'Filename';

            % Create FilenameEditField
            app.FilenameEditField = uieditfield(app.UIFigure, 'text');
            app.FilenameEditField.Position = [94 442 497 22];

            % Create unfoldbandstrCheckBox
            app.unfoldbandstrCheckBox = uicheckbox(app.UIFigure);
            app.unfoldbandstrCheckBox.Text = 'unfold bandstr';
            app.unfoldbandstrCheckBox.Position = [375 350 98 22];

            % Create atomgroupDropDownLabel
            app.atomgroupDropDownLabel = uilabel(app.UIFigure);
            app.atomgroupDropDownLabel.HorizontalAlignment = 'right';
            app.atomgroupDropDownLabel.Position = [290 384 66 22];
            app.atomgroupDropDownLabel.Text = 'atom group';

            % Create atomgroupDropDown
            app.atomgroupDropDown = uidropdown(app.UIFigure);
            app.atomgroupDropDown.Items = {'all'};
            app.atomgroupDropDown.ItemsData = {'1'};
            app.atomgroupDropDown.Position = [371 384 100 22];
            app.atomgroupDropDown.Value = '1';

            % Create plotatomicstructureButton
            app.plotatomicstructureButton = uibutton(app.UIFigure, 'push');
            app.plotatomicstructureButton.ButtonPushedFcn = createCallbackFcn(app, @plotatomicstructureButtonPushed, true);
            app.plotatomicstructureButton.Position = [350 320 123 22];
            app.plotatomicstructureButton.Text = 'plot atomic structure';

            % Create savePDFCheckBox
            app.savePDFCheckBox = uicheckbox(app.UIFigure);
            app.savePDFCheckBox.Text = 'save PDF';
            app.savePDFCheckBox.Position = [491 220 75 22];

            % Create saveplotdataCheckBox
            app.saveplotdataCheckBox = uicheckbox(app.UIFigure);
            app.saveplotdataCheckBox.Text = 'save plot data';
            app.saveplotdataCheckBox.Position = [491 64 97 22];

            % Create NameEditFieldLabel
            app.NameEditFieldLabel = uilabel(app.UIFigure);
            app.NameEditFieldLabel.HorizontalAlignment = 'right';
            app.NameEditFieldLabel.Position = [464 195 38 22];
            app.NameEditFieldLabel.Text = 'Name';

            % Create NameEditField
            app.NameEditField = uieditfield(app.UIFigure, 'text');
            app.NameEditField.Position = [517 195 100 22];

            % Create yMinEditFieldLabel
            app.yMinEditFieldLabel = uilabel(app.UIFigure);
            app.yMinEditFieldLabel.HorizontalAlignment = 'right';
            app.yMinEditFieldLabel.Position = [472 162 31 22];
            app.yMinEditFieldLabel.Text = 'yMin';

            % Create yMinEditField
            app.yMinEditField = uieditfield(app.UIFigure, 'numeric');
            app.yMinEditField.ValueDisplayFormat = '%.2f';
            app.yMinEditField.Position = [517 162 100 22];

            % Create yMaxEditFieldLabel
            app.yMaxEditFieldLabel = uilabel(app.UIFigure);
            app.yMaxEditFieldLabel.HorizontalAlignment = 'right';
            app.yMaxEditFieldLabel.Position = [470 130 34 22];
            app.yMaxEditFieldLabel.Text = 'yMax';

            % Create yMaxEditField
            app.yMaxEditField = uieditfield(app.UIFigure, 'numeric');
            app.yMaxEditField.ValueDisplayFormat = '%.2f';
            app.yMaxEditField.Position = [517 130 100 22];

            % Create jspDropDownLabel
            app.jspDropDownLabel = uilabel(app.UIFigure);
            app.jspDropDownLabel.HorizontalAlignment = 'right';
            app.jspDropDownLabel.Position = [286 350 25 22];
            app.jspDropDownLabel.Text = 'jsp';

            % Create jspDropDown
            app.jspDropDown = uidropdown(app.UIFigure);
            app.jspDropDown.Items = {'1'};
            app.jspDropDown.Position = [314 350 52 22];
            app.jspDropDown.Value = '1';

            % Create UnfoldingIntensitySliderLabel
            app.UnfoldingIntensitySliderLabel = uilabel(app.UIFigure);
            app.UnfoldingIntensitySliderLabel.HorizontalAlignment = 'right';
            app.UnfoldingIntensitySliderLabel.Position = [297 298 104 22];
            app.UnfoldingIntensitySliderLabel.Text = 'Unfolding Intensity';

            % Create UnfoldingIntensitySlider
            app.UnfoldingIntensitySlider = uislider(app.UIFigure);
            app.UnfoldingIntensitySlider.Limits = [0 4];
            app.UnfoldingIntensitySlider.MajorTicks = [0 1 2 3 4];
            app.UnfoldingIntensitySlider.MajorTickLabels = {'0', '1', '2', '3', '4'};
            app.UnfoldingIntensitySlider.Tooltip = {'this defines an exponent which is multiplied with the unfolding weight ( between 0 and 4)'};
            app.UnfoldingIntensitySlider.Position = [296 290 150 3];
            app.UnfoldingIntensitySlider.Value = 1.5;

            % Create backgroundCheckBox
            app.backgroundCheckBox = uicheckbox(app.UIFigure);
            app.backgroundCheckBox.Text = 'background';
            app.backgroundCheckBox.Position = [491 246.999998092651 85 22];

            % Create pointsizeEditFieldLabel
            app.pointsizeEditFieldLabel = uilabel(app.UIFigure);
            app.pointsizeEditFieldLabel.HorizontalAlignment = 'right';
            app.pointsizeEditFieldLabel.Position = [502 101 56 22];
            app.pointsizeEditFieldLabel.Text = 'point size';

            % Create pointsizeEditField
            app.pointsizeEditField = uieditfield(app.UIFigure, 'numeric');
            app.pointsizeEditField.Limits = [0 Inf];
            app.pointsizeEditField.ValueDisplayFormat = '%.0f';
            app.pointsizeEditField.Position = [573 100 43 22];
            app.pointsizeEditField.Value = 36;
        end
    end

    methods (Access = public)

        % Construct app
        function app = banddos_analysis_1

            % Create and configure components
            createComponents(app)

            % Register the app with App Designer
            registerApp(app, app.UIFigure)

            if nargout == 0
                clear app
            end
        end

        % Code that executes before app deletion
        function delete(app)

            % Delete UIFigure when app is deleted
            delete(app.UIFigure)
        end
    end
end
