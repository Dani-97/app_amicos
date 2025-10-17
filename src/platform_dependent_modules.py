class PlatformDependentModulesFactory():
    
    def __init__(self):
        pass

    def create_modules_provider(self, platform):
        if (platform=='android'):
            return AndroidModulesProvider()
        else:
            return BaseModulesProvider()

class BaseModulesProvider():

    def __init__(self):
        pass

    def text_to_speech(self, message, locale):
        raise NotImplementedError('Text to speech is not implemented for your current platform.')

class AndroidModulesProvider(BaseModulesProvider):

    def __init__(self):
        from jnius import autoclass

        self.PythonActivity = autoclass('org.kivy.android.PythonActivity')
        TextToSpeech = autoclass('android.speech.tts.TextToSpeech')
        self.Locale = autoclass('java.util.Locale')
        self.Bundle = autoclass('android.os.Bundle')
        self.JavaString = autoclass('java.lang.String')

        activity = self.PythonActivity.mActivity
        self.tts_engine = TextToSpeech(activity, None)

    def text_to_speech(self, message, locale):
        current_language = locale[0]
        current_country = locale[1]
        status = self.tts_engine.setLanguage(self.Locale(current_language, current_country))

        message_java_string = self.JavaString(message)
        params = self.Bundle()
        utterance_id = self.JavaString("utterance1")
        self.tts_engine.speak(
            message_java_string,
            self.tts_engine.QUEUE_FLUSH,
            params,
            utterance_id
        )