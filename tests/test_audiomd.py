"""Unit tests for creation of AudioMD metadata.
"""

import pytest
import audiomd.audiomd as amd

NAMESPACES = {'amd': amd.AUDIOMD_NS}


def test_audiomd():
    """Test that audiomd() functions returns the root XML elements with
    correct metadata.
    """

    compression = amd.amd_compression(app='SoundForge',
                                      app_version='10',
                                      name='(:unap)',
                                      quality='lossy')

    params = amd.get_params(amd.FILE_DATA_PARAMS)
    params["audioDataEncoding"] = ["PCM"]
    params["bitsPerSample"] = ["8"]
    params["Compression"] = [compression]
    params["dataRate"] = ["256"]
    params["dataRateMode"] = ["Fixed"]
    params["samplingFrequency"] = ["44.1"]

    file_data = amd.amd_file_data(params)
    audio_info = amd.amd_audio_info(duration=['PT1H30M'], num_channels=['1'])
    audiomd = amd.audiomd(file_data=file_data, audio_info=audio_info)

    path = "/amd:amd[@ANALOGDIGITALFLAG='FileDigital']"
    assert len(audiomd.xpath(path, namespaces=NAMESPACES)) == 1

    path = "/amd:amd/amd:fileData/amd:audioDataEncoding"
    assert audiomd.xpath(path, namespaces=NAMESPACES)[0].text == 'PCM'

    path = "/amd:amd/amd:fileData/amd:bitsPerSample"
    assert audiomd.xpath(path, namespaces=NAMESPACES)[0].text == '8'

    path = "/amd:amd/amd:fileData/amd:compression/amd:codecCreatorApp"
    assert audiomd.xpath(path, namespaces=NAMESPACES)[0].text == 'SoundForge'

    path = "/amd:amd/amd:fileData/amd:compression/amd:codecCreatorAppVersion"
    assert audiomd.xpath(path, namespaces=NAMESPACES)[0].text == '10'

    path = "/amd:amd/amd:fileData/amd:compression/amd:codecName"
    assert audiomd.xpath(path, namespaces=NAMESPACES)[0].text == '(:unap)'

    path = "/amd:amd/amd:fileData/amd:compression/amd:codecQuality"
    assert audiomd.xpath(path, namespaces=NAMESPACES)[0].text == 'lossy'

    path = "/amd:amd/amd:fileData/amd:dataRate"
    assert audiomd.xpath(path, namespaces=NAMESPACES)[0].text == '256'

    path = "/amd:amd/amd:fileData/amd:dataRateMode"
    assert audiomd.xpath(path, namespaces=NAMESPACES)[0].text == 'Fixed'

    path = "/amd:amd/amd:fileData/amd:samplingFrequency"
    assert audiomd.xpath(path, namespaces=NAMESPACES)[0].text == '44.1'

    path = "/amd:amd/amd:audioInfo/amd:duration"
    assert audiomd.xpath(path, namespaces=NAMESPACES)[0].text == 'PT1H30M'

    path = "/amd:amd/amd:audioInfo/amd:numChannels"
    assert audiomd.xpath(path, namespaces=NAMESPACES)[0].text == '1'


def test_audiomd_param_fail():
    """Test that ValueError is raised if any of the provided
    parameters is not recognized.
    """

    params = {"typo" : None}

    with pytest.raises(ValueError):
        amd.amd_file_data(params)

    with pytest.raises(ValueError):
        amd.amd_physical_data(params)

    with pytest.raises(ValueError):
        amd.amd_dimensions(params)

    with pytest.raises(ValueError):
        amd.amd_material(params)


def test_file_data():
    """Test that amd_file_data() produces correct XML element
    """
    pass


def test_message_digest():
    """Test that amd_message_digest() produces correct XML element
    """
    pass


def test_compression():
    """Test that amd_compression() produces correct XML element
    """
    pass


def test_physical_data():
    """Test that amd_physical_data() produces correct XML element
    """
    pass


def test_dimensions():
    """Test that amd_dimensions() produces correct XML element
    """
    pass


def test_material():
    """Test that amd_material() produces correct XML element
    """
    pass


def test_tracking():
    """Test that amd_tracking() produces correct XML element
    """
    pass


def test_audio_info():
    """Test that amd_audio_info() produces correct XML element
    """
    pass


def test_sound_channel_map():
    """Test that amd_sound_channel_map() produces correct XML element
    """
    pass


def test_calibration_info():
    """Test that amd_calibration_info() produces correct XML element
    """
    pass
