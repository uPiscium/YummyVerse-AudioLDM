# import subprocess
from diffusers import AudioLDM2Pipeline
import torch
import scipy
import numpy


class AudioLDM2Controller:
    """
    A class to handle the AudioLDM2 pipeline for audio generation.
    Inherits from VitsModel to utilize its functionalities.
    """

    def __init__(self, repo_id: str = "cvssp/audioldm2"):
        """
        Initialize the AudioLDM2Pipeline with the specified model name.

        Args:
            model_name (str): The name of the AudioLDM2 model to use.
        """
        self.model = AudioLDM2Pipeline.from_pretrained(
            repo_id, torch_dtype=torch.float16
        )
        self.model = self.model.to("cuda")

    def generate_audio(
        self,
        prompt: str,
        num_inference_steps: int = 200,
        length_s: float = 10.0,
    ) -> numpy.ndarray:
        """
        Generate audio based on the provided text prompt.

        Args:
            prompt_embedding (tuple): The embedding of the text prompt.
            num_inference_steps (int): The number of inference steps for the generation.
            audio_length_in_s (float): The desired length of the generated audio in seconds.

        Returns:
            numpy.ndarray: The generated audio data.
        """
        audio = self.model(
            prompt=prompt,
            num_inference_steps=num_inference_steps,
            audio_length_in_s=length_s,
        ).audios[0]
        return audio

    def save_audio(self, audio: numpy.ndarray, filename: str):
        """
        Save the generated audio to a file.

        Args:
            audio (numpy.ndarray): The generated audio data.
            filename (str): The name of the file to save the audio to.
        """
        scipy.io.wavfile.write(filename, rate=16000, data=audio)
