"""Functions for reading and generating AudioMD Data Dictionaries as
xml.etree.ElementTree data structures.

References:

    * AudioMD https://www.loc.gov/standards/amdvmd/
    * Schema documentation: https://www.loc.gov/standards/amdvmd/htmldoc/audioMD.html
    * ElementTree
    https://docs.python.org/2.6/library/xml.etree.elementtree.html

"""


import lxml.etree as ET
from xml_helpers.utils import xsi_ns, XSI_NS


AUDIOMD_NS = 'http://www.loc.gov/audioMD/'
NAMESPACE = {"amd" : AUDIOMD_NS, "xsi" : XSI_NS}

FILE_DATA_PARAMS = [
    "audioBlockSize", "audioDataEncoding", "bitsPerSample",
    "byteOrder", "messageDigest", "compression",
    "dataRate", "dataRateMode", "firstSampleOffset",
    "firstValidByteBlock", "formatLocation", "formatName",
    "formatNote", "formatVersion", "lastValidByteBlock",
    "numSampleFrames", "samplingFrequency", "security",
    "use", "otherUse", "wordSize"
]


PHYSICAL_DATA_PARAMS = [
    "EBUStorageMediaCodes", "condition", "dimensions",
    "disposition", "equalization", "generation",
    "groove", "material", "noiseReduction",
    "physFormat", "speed", "speedAdjustment",
    "speedNote", "trackFormat", "tracking",
    "note"
]


DIMENSIONS_PARAMS = [
    "DEPTH", "DIAMETER", "GAUGE",
    "HEIGHT", "LENGTH", "NOTE",
    "THICKNESS", "UNITS", "WIDTH"
]

MATERIAL_PARAMS = [
    "baseMaterial", "binder", "discSurface",
    "oxide", "activeLayer", "reflectiveLayer",
    "stockBrand", "method", "usedSides"
]


def audiomd_ns(tag, prefix=""):
    """Prefix ElementTree tags with audioMD namespace.

    object -> {http://www.loc.gov/audioMD}object

    :tag: Tag name as string
    :returns: Prefixed tag

    """
    if prefix:
        tag = tag[0].upper() + tag[1:]
        return '{%s}%s%s' % (AUDIOMD_NS, prefix, tag)
    return '{%s}%s' % (AUDIOMD_NS, tag)


def _element(tag, prefix=""):
    """Return _ElementInterface with audioMD namespace.

    Prefix parameter is useful for adding prefixed to lower case tags. It just
    uppercases first letter of tag and appends it to prefix::

        element = _element('objectIdentifier', 'linking')
        element.tag
        'linkingObjectIdentifier'

    :tag: Tagname
    :prefix: Prefix for the tag (default="")
    :returns: ElementTree element object

    """
    return ET.Element(audiomd_ns(tag, prefix), nsmap=NAMESPACE)


def _subelement(parent, tag, prefix=""):
    """Return subelement for the given parent element. Created element is
    appelded to parent element.

    :parent: Parent element
    :tag: Element tagname
    :prefix: Prefix for the tag
    :returns: Created subelement

    """
    return ET.SubElement(parent, audiomd_ns(tag, prefix))


def _simple_elements(parent, elements, element_name):
    if elements is not None:

        if isinstance(elements, list):
            for element in elements:
                amd_element = _subelement(parent, element_name)
                amd_element.text = element
        else:
            amd_element = _subelement(parent, element_name)
            amd_element.text = elements


def _add_elements(parent, elements):
    if elements is not None:

        if isinstance(elements, list):
            for element in elements:
                parent.append(element)
        else:
            parent.append(elements)


def get_params(param_list):
    """Initialize all parameters as None

    :returns: Dict of parameters
    """

    params = {}
    for key in param_list:
        params[key] = None

    return params


def _check_params(param_dict, param_list):
    """Check that all the provided parameters in param_dict
    are found in the param_list.
    """

    for key in param_dict:
        if key not in param_list:
            raise ValueError("Parameter: '%s' not recognized" % key)


def create_audiomd(analog_digital_flag='FileDigital', file_data=None,
                   physical_data=None, audio_info=None, calibration_info=None):
    """Create audioMD Data Dictionary root element.

    :Schema documentation: https://www.loc.gov/standards/amdvmd/audiovideoMDschemas.html
    :child_elements: Any elements appended to the audioMD dictionary

    Returns the following ElementTree structure::


        <amd:AUDIOMD
            xmlns:amd="http://www.loc.gov/audioMD/"

    """
    audiomd_elem = _element('AUDIOMD')
    audiomd_elem.set(
        xsi_ns('schemaLocation'),
        'http://www.loc.gov/audioMD/ ' +
        'https://www.loc.gov/standards/amdvmd/audioMD.xsd'
    )
    audiomd_elem.set('ANALOGDIGITALFLAG', analog_digital_flag)

    if file_data is not None:
        audiomd_elem.append(file_data)
    if physical_data is not None:
        audiomd_elem.append(physical_data)
    if audio_info is not None:
        audiomd_elem.append(audio_info)
    if calibration_info is not None:
        audiomd_elem.append(calibration_info)

    return audiomd_elem


def amd_file_data(params):
    """Returns AudioMD fileData element

    :Schema documentation: https://www.loc.gov/standards/amdvmd/audiovideoMDschemas.html

    Returns the following ElementTree structure::

        <amd:fileData>
            <amd:audioBlockSize></amd:audioBlockSize>
            <amd:audioDataEncoding></amd:audioDataEncoding>
            <amd:bitsPerSample></amd:bitsPerSample>
            <amd:byteOrder></amd:byteOrder>
            {{ messageDigest elements }}
            {{ compression elements }}
            <amd:dataRate></amd:dataRate>
            <amd:dataRateMode></amd:dataRateMode>
            <amd:firstSampleOffset></amd:firstSampleOffset>
            <amd:firstValidByteBlock></amd:firstValidByteBlock>
            <amd:formatLocation></amd:formatLocation>
            <amd:formatName></amd:formatName>
            <amd:formatNote></amd:formatNote>
            <amd:formatVersion></amd:formatVersion>
            <amd:lastValidByteBlock></amd:lastValidByteBlock>
            <amd:numSampleFrames></amd:numSampleFrames>
            <amd:samplingFrequency></amd:samplingFrequency>
            <amd:security></amd:security>
            <amd:use></amd:use>
            <amd:otherUse></amd:otherUse>
            <amd:wordSize></amd:wordSize>
        </amd:fileData>

    """
    _check_params(params, FILE_DATA_PARAMS)

    element = _element('fileData')

    for key in FILE_DATA_PARAMS:
        if key in params:
            if key == "messageDigest" or key == "compression":
                _add_elements(element, params[key])
            else:
                _simple_elements(element, params[key], key)

    return element


def amd_message_digest(datetime, algorithm, message_digest):
    """Returns AudioMD messageDigest element

    :Schema documentation: https://www.loc.gov/standards/amdvmd/audiovideoMDschemas.html

    Returns the following ElementTree structure::

        <amd:messageDigest>
            <amd:messageDigestDatetime></amd:messageDigestDatetime>
            <amd:messageDigestAlgorithm></amd:messageDigestAlgorithm>
            <amd:messageDigest></amd:messageDigest>
        </amd:messageDigest>

    """
    message_digest_elem = _element('messageDigest')

    datetime_elem = _subelement(message_digest_elem, 'messageDigestDatetime')
    datetime_elem.text = datetime

    algorithm_elem = _subelement(message_digest_elem, 'messageDigestAlgorithm')
    algorithm_elem.text = algorithm

    message_digest_value_elem = _subelement(message_digest_elem, 'messageDigest')
    message_digest_value_elem.text = message_digest

    return message_digest_elem


def amd_compression(app=None, app_version=None, name=None, quality=None):
    """Returns AudioMD compression element

    :Schema documentation: https://www.loc.gov/standards/amdvmd/audiovideoMDschemas.html

    Returns the following ElementTree structure::

        <amd:compression>
            <amd:codecCreatorApp></amd:codecCreatorApp>
            <amd:codecCreatorAppVersion></amd:codecCreatorAppVersion>
            <amd:codecName></amd:codecName>
            <amd:codecQuality></amd:codecQuality>
        </amd:compression>

    """
    compression_elem = _element('compression')

    _simple_elements(compression_elem, app, 'codecCreatorApp')
    _simple_elements(compression_elem, app_version, 'codecCreatorAppVersion')
    _simple_elements(compression_elem, name, 'codecName')
    _simple_elements(compression_elem, quality, 'codecQuality')

    return compression_elem


def amd_physical_data(params):
    """Returns AudioMD physicalData element

    :Schema documentation: https://www.loc.gov/standards/amdvmd/audiovideoMDschemas.html

    Returns the following ElementTree structure::

        <amd:physicalData>
            <amd:EBUStorageMediaCodes></amd:EBUStorageMediaCodes>
            <amd:condition></amd:condition>
            << dimensions elements >>
            <amd:disposition></amd:disposition>
            <amd:equalization></amd:equalization>
            <amd:generation></amd:generation>
            <amd:groove></amd:groove>
            << material elements >>
            <amd:noiseReduction></amd:noiseReduction>
            <amd:physFormat></amd:physFormat>
            <amd:speed></amd:speed>
            <amd:speedAdjustment></amd:speedAdjustment>
            <amd:speedNote></amd:speedNote>
            <amd:trackFormat></amd:trackFormat>
            << tracking elements >>
            <amd:note></amd:note>
        </amd:physicalData>

    """
    _check_params(params, PHYSICAL_DATA_PARAMS)

    physical_data_elem = _element('physicalData')

    for key in PHYSICAL_DATA_PARAMS:
        if key in params:
            if key in ["dimensions", "material", "tracking"]:
                _add_elements(physical_data_elem, params[key])
            else:
                _simple_elements(physical_data_elem, params[key], key)

    return physical_data_elem


def amd_dimensions(params):
    """Returns AudioMD dimensions element

    :Schema documentation: https://www.loc.gov/standards/amdvmd/audiovideoMDschemas.html

    Returns the following ElementTree structure::

        <amd:dimensions DEPTH="" DIAMETER="" GAUGE="" HEIGHT="" LENGTH=""
            NOTE="" THICKNESS="" UNITS="" WIDTH="">
        </amd:dimensions>

    """
    _check_params(params, DIMENSIONS_PARAMS)

    dimensions_elem = _element('dimensions')

    for key in DIMENSIONS_PARAMS:
        if key in params and params[key] is not None:
            dimensions_elem.set(key, params[key])

    return dimensions_elem


def amd_material(params):
    """Returns AudioMD material element

    :Schema documentation: https://www.loc.gov/standards/amdvmd/audiovideoMDschemas.html

    Returns the following ElementTree structure::

        <amd:material>
            <amd:baseMaterial></amd:baseMaterial>
            <amd:binder></amd:binder>
            <amd:discSurface></amd:discSurface>
            <amd:oxide></amd:oxide>
            <amd:activeLayer></amd:activeLayer>
            <amd:reflectiveLayer></amd:reflectiveLayer>
            <amd:stockBrand></amd:stockBrand>
            <amd:method></amd:method>
            <amd:usedSides></amd:usedSides>
        </amd:material>
    """
    _check_params(params, MATERIAL_PARAMS)

    material_elem = _element('material')

    for key in MATERIAL_PARAMS:
        if key in params:
            _simple_elements(material_elem, params[key], key)

    return material_elem


def amd_tracking(tracking_type=None, tracking_value=None):
    """Returns AudioMD tracking element

    :Schema documentation: https://www.loc.gov/standards/amdvmd/audiovideoMDschemas.html

    Returns the following ElementTree structure::

        <amd:tracking>
            <amd:trackingType></amd:trackingType>
            <amd:trackingValue></amd:trackingValue>
        </amd:tracking>

    """
    tracking_elem = _element('tracking')

    _simple_elements(tracking_elem, tracking_type, 'trackingType')
    _simple_elements(tracking_elem, tracking_value, 'trackingValue')

    return tracking_elem


def amd_audio_info(
        duration=None, note=None, num_channels=None,
        sound_channel_map=None, sound_field=None
):
    """Returns AudioMD audioInfo element

    :Schema documentation: https://www.loc.gov/standards/amdvmd/audiovideoMDschemas.html

    Returns the following ElementTree structure::

        <amd:audioInfo>
            <amd:duration></amd:duration>
            <amd:note></amd:note>
            <amd:numChannels></amd:numChannels>
            << soundChannelMap elements >>
            <amd:soundField></amd:soundField>
        </amd:audioInfo>

    """
    audio_info_elem = _element('audioInfo')

    _simple_elements(audio_info_elem, duration, 'duration')
    _simple_elements(audio_info_elem, note, 'note')
    _simple_elements(audio_info_elem, num_channels, 'numChannels')
    _add_elements(audio_info_elem, sound_channel_map)
    _simple_elements(audio_info_elem, sound_field, 'soundField')

    return audio_info_elem


def amd_sound_channel_map(channelnum=None, maplocation=None):
    """Returns soundChannelMap dimensions element

    :Schema documentation: https://www.loc.gov/standards/amdvmd/audiovideoMDschemas.html

    Returns the following ElementTree structure::

        <amd:soundChannelMap>
            <amd:channelAssignment CHANNELNUM="" MAPLOCATION="">
            </amd:channelAssignment>
        <amd:soundChannelMap>

    """

    sound_channel_map_elem = _element('soundChannelMap')
    channel_assignment_elem = _subelement(
        sound_channel_map_elem,
        'channelAssignment'
    )

    if channelnum is not None:
        channel_assignment_elem.set('CHANNELNUM', channelnum)
    if maplocation is not None:
        channel_assignment_elem.set('MAPLOCATION', maplocation)

    return sound_channel_map_elem


def amd_calibration_info(
        ext_int=None, location=None,
        time_stamp=None, track_type=None
):
    """Returns AudioMD calibrationInfo element

    :Schema documentation: https://www.loc.gov/standards/amdvmd/audiovideoMDschemas.html

    Returns the following ElementTree structure::

        <amd:calibrationInfo>
            <amd:calibrationExtInt></amd:calibrationExtInt>
            <amd:calibrationLocation></amd:calibrationLocation>
            <amd:calibrationTimeStamp></amd:calibrationTimeStamp>
            <amd:calibrationTrackType></amd:calibrationTrackType>
        </amd:calibrationInfo>
    """

    calibration_info_elem = _element('calibrationInfo')

    _simple_elements(calibration_info_elem, ext_int, 'calibrationExtInt')
    _simple_elements(calibration_info_elem, location, 'calibrationLocation')
    _simple_elements(calibration_info_elem, time_stamp, 'calibrationTimeStamp')
    _simple_elements(calibration_info_elem, track_type, 'calibrationTrackType')

    return calibration_info_elem
