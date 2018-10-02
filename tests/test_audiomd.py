"""Unit tests for creation of AudioMD metadata.
"""

import pytest
import audiomd as amd

NAMESPACES = {'amd': amd.AUDIOMD_NS}


def _get_elems(root, path):
    return root.xpath(path, namespaces=NAMESPACES)


def test_audiomd():
    """Test that create_audiomd() functions returns the
    root XML elements with correct metadata.
    """

    compression = amd.amd_compression(
        app='(:unap)',
        app_version='(:unap)',
        name='(:unap)',
        quality='lossless'
    )

    params = amd.get_params(amd.FILE_DATA_PARAMS)
    params["audioDataEncoding"] = "PCM"
    params["bitsPerSample"] = "8"
    params["Compression"] = compression
    params["dataRate"] = "256"
    params["dataRateMode"] = "Fixed"
    params["samplingFrequency"] = "44.1"

    file_data = amd.amd_file_data(params)
    audio_info = amd.amd_audio_info(duration=['PT1H30M'], num_channels=['1'])
    audiomd = amd.create_audiomd(file_data=file_data, audio_info=audio_info)

    path = "/amd:amd[@ANALOGDIGITALFLAG='FileDigital']"
    assert len(audiomd.xpath(path, namespaces=NAMESPACES)) == 1

    path = "/amd:amd/amd:fileData/amd:audioDataEncoding"
    assert audiomd.xpath(path, namespaces=NAMESPACES)[0].text == 'PCM'

    path = "/amd:amd/amd:fileData/amd:bitsPerSample"
    assert audiomd.xpath(path, namespaces=NAMESPACES)[0].text == '8'

    path = "/amd:amd/amd:fileData/amd:compression/amd:codecCreatorApp"
    assert audiomd.xpath(path, namespaces=NAMESPACES)[0].text == '(:unap)'

    path = "/amd:amd/amd:fileData/amd:compression/amd:codecCreatorAppVersion"
    assert audiomd.xpath(path, namespaces=NAMESPACES)[0].text == '(:unap)'

    path = "/amd:amd/amd:fileData/amd:compression/amd:codecName"
    assert audiomd.xpath(path, namespaces=NAMESPACES)[0].text == '(:unap)'

    path = "/amd:amd/amd:fileData/amd:compression/amd:codecQuality"
    assert audiomd.xpath(path, namespaces=NAMESPACES)[0].text == 'lossless'

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


def test_message_digest():
    """Test that amd_message_digest() produces correct XML element
    """
    root = amd.amd_message_digest("datetime", "algorithm", "message")

    path = "/amd:messageDigest/amd:messageDigest"

    message = _get_elems(root, path)[0].text
    datetime = _get_elems(root, path + "Datetime")[0].text
    algorithm = _get_elems(root, path + "Algorithm")[0].text

    assert message == "message"
    assert datetime == "datetime"
    assert algorithm == "algorithm"


def test_compression():
    """Test that amd_compression() produces correct XML element
    """
    root = amd.amd_compression("app", "app_version", "name", "quality")

    path = "/amd:compression/amd:codec"

    app = _get_elems(root, path + "CreatorApp")[0].text
    app_version = _get_elems(root, path + "CreatorAppVersion")[0].text
    name = _get_elems(root, path + "Name")[0].text
    quality = _get_elems(root, path + "Quality")[0].text

    assert app == "app"
    assert app_version == "app_version"
    assert name == "name"
    assert quality == "quality"


def test_physical_data():
    """Test that amd_physical_data() produces correct XML element
    """
    params = amd.get_params(amd.PHYSICAL_DATA_PARAMS)
    params["condition"] = "condition"
    params["disposition"] = "disposition"

    root = amd.amd_physical_data(params)

    path = "/amd:physicalData/amd:"

    condition = _get_elems(root, path + "condition")[0].text
    disposition = _get_elems(root, path + "disposition")[0].text

    assert condition == "condition"
    assert disposition == "disposition"


def test_dimensions():
    """Test that amd_dimensions() produces correct XML element
    """
    params = {"DEPTH" : "DEPTH", "DIAMETER" : "DIAMETER"}

    root = amd.amd_dimensions(params)

    assert root.get("DEPTH") == "DEPTH"
    assert root.get("DIAMETER") == "DIAMETER"


def test_material():
    """Test that amd_material() produces correct XML element
    """
    params = amd.get_params(amd.MATERIAL_PARAMS)
    params["baseMaterial"] = "baseMaterial"
    params["binder"] = "binder"

    root = amd.amd_material(params)

    path = "/amd:material/amd:"

    base_material = _get_elems(root, path + "baseMaterial")[0].text
    binder = _get_elems(root, path + "binder")[0].text

    assert base_material == "baseMaterial"
    assert binder == "binder"


def test_tracking():
    """Test that amd_tracking() produces correct XML element
    """
    root = amd.amd_tracking("trackingType", "trackingValue")
    path = "/amd:tracking/amd:tracking"

    tracking_type = _get_elems(root, path + "Type")[0].text
    tracking_value = _get_elems(root, path + "Value")[0].text

    assert tracking_type == "trackingType"
    assert tracking_value == "trackingValue"


def test_sound_channel_map():
    """Test that amd_sound_channel_map() produces correct XML element
    """
    root = amd.amd_sound_channel_map("CHANNELNUM", "MAPLOCATION")
    assignment = root[0]

    assert assignment.get("CHANNELNUM") == "CHANNELNUM"
    assert assignment.get("MAPLOCATION") == "MAPLOCATION"


def test_calibration_info():
    """Test that amd_calibration_info() produces correct XML element
    """
    root = amd.amd_calibration_info("ExtInt", "Location")
    path = "/amd:calibrationInfo/amd:calibration"

    ext_int = _get_elems(root, path + "ExtInt")[0].text
    location = _get_elems(root, path + "Location")[0].text

    assert ext_int == "ExtInt"
    assert location == "Location"
