close all
SampleRate = 600; 

overall_time_in_sec = (size(EEG.data,2) / SampleRate) 
overall_time_in_min = (size(EEG.data,2) / SampleRate) / 60

t = (0:length(EEG.data(1,:))-1) / SampleRate; % Time vector
start_sec = 20;
end_sec = 25;

start_idx = start_sec * SampleRate + 1;
end_idx = end_sec * SampleRate;

%%% x/y for both eyes
figure;
subplot(4, 1, 1);
plot(t(start_idx:end_idx), EEG.data(3,start_idx:end_idx), 'b'); 
subplot(4, 1, 2);
plot(t(start_idx:end_idx), EEG. data(4,start_idx:end_idx), 'b'); 
subplot(4, 1, 3);
plot(t(start_idx:end_idx), EEG.data(5,start_idx:end_idx), 'r'); 
subplot(4, 1, 4);
plot(t(start_idx:end_idx), EEG. data(6,start_idx:end_idx), 'r'); 

%%% pupilometry
figure;
subplot(4, 1, 1);
plot(t(start_idx:end_idx), EEG.data(7,start_idx:end_idx), 'b'); 
subplot(4, 1, 2);
plot(t(start_idx:end_idx), EEG. data(8,start_idx:end_idx), 'b'); 
subplot(4, 1, 3);
plot(t(start_idx:end_idx), EEG.data(9,start_idx:end_idx), 'r'); 
subplot(4, 1, 4);
plot(t(start_idx:end_idx), EEG. data(10,start_idx:end_idx), 'r');

%%% validity
figure;
subplot(4, 1, 1);
plot(t(start_idx:end_idx), EEG.data(11,start_idx:end_idx), 'b'); 
subplot(4, 1, 2);
plot(t(start_idx:end_idx), EEG. data(13,start_idx:end_idx), 'b'); 
subplot(4, 1, 3);
plot(t(start_idx:end_idx), EEG.data(12,start_idx:end_idx), 'r'); 
subplot(4, 1, 4);
plot(t(start_idx:end_idx), EEG. data(14,start_idx:end_idx), 'r'); 
