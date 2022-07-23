function [training]=checksequence()
files=getfolder;
            
             files_pre_training=files((contains(files,['pre']) | contains(files,['Pre'])) &  ~contains(files,['test']) &  ~contains(files,['Test'])    );
             if length(files_pre_training)>1
                files_pre_training=files_pre_training(contains(files_pre_training,'merged'));
             end

%              files_post_training=files(contains(files,['post']) & ~contains(files,['trial6']));
             files_post_training1=files((contains(files,['post']) | contains(files,['Post'])) & (contains(files,['trial1']) | contains(files,['Trial1']) ) );
             if length(files_post_training1)>1
                files_post_training1=files_post_training1(contains(files_post_training1,'merged'));
             end

             files_post_training2=files((contains(files,['post']) | contains(files,['Post'])) & (contains(files,['trial2']) | contains(files,['Trial2']) ) ) ;
             if length(files_post_training2)>1
                files_post_training2=files_post_training2(contains(files_post_training2,'merged'));
             end

             files_post_training3=files((contains(files,['post']) | contains(files,['Post'])) & (contains(files,['trial3']) |contains(files,['Trial3']) ) ) ;
             if length(files_post_training3)>1
                files_post_training3=files_post_training3(contains(files_post_training3,'merged'));
             end

             files_post_training4=files((contains(files,['post']) | contains(files,['Post'])) & (contains(files,['trial4'])  | contains(files,['Trial4']) ) );
             if length(files_post_training4)>1
                files_post_training4=files_post_training4(contains(files_post_training4,'merged'));
             end

             files_post_training5=files((contains(files,['post']) |  contains(files,['Post'])) & (contains(files,['trial5']) | contains(files,['Trial5']) ) );
             if length(files_post_training5)>1
                files_post_training5=files_post_training5(contains(files_post_training5,'merged'));
             end


             training=[files_pre_training files_post_training1 files_post_training2 files_post_training3 files_post_training4 files_post_training5].'

h=questdlg('Check that trial sequence is correct','Warning','OK','OK');
switch h
  case 'OK'
     %'OK' code here
  case ''
     %abort code
  otherwise
end

training=training.';
return
end