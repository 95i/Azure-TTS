from azure.cognitiveservices.speech import AudioDataStream, SpeechSynthesizer
import azure.cognitiveservices.speech as speechsdk

# 替换下面的speech_key，service_region
speech_key, service_region = "speech_key", "service_region"
speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region)
# 默认运行中不播放音频，如果需要运行中播放音频请把audio_config删掉
speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=None)

text = "你吃饭了吗？我现在声音自然多了吧"
with open('text.txt', 'r',encoding='utf-8',errors='ignore') as f:
   text = f.read()

# SSML中需要书签标签，例如。
ssml = "<speak version='1.0' xml:lang='zh-CN' xmlns='http://www.w3.org/2001/10/synthesis' xmlns:mstts='http://www.w3.org/2001/mstts'><voice name='zh-cn-XiaohanNeural'><bookmark mark='bookmark_one'/> {} </voice></speak>" .format(text)
result = speech_synthesizer.speak_ssml_async(ssml).get() #这个是/SSML文本

if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
    stream = AudioDataStream(result)
    # 如果把上面的audio_config删掉了，请使用下面这行进行保存文件
    # stream.save_to_wav_file("file.wav")
    运行后保存文件
    stream.save_to_wav_file_async("file.wav")
    print("Speech synthesized.")
elif result.reason == speechsdk.ResultReason.Canceled:
    cancellation_details = result.cancellation_details
    print("Speech synthesis canceled: {}".format(cancellation_details.reason))
    if cancellation_details.reason == speechsdk.CancellationReason.Error:
        print("Error details: {}".format(cancellation_details.error_details))
