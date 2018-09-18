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


AudioMD_NS = 'http://www.loc.gov/audioMD/'


def audiomd_ns(tag, prefix=""):
    """Prefix ElementTree tags with audioMD namespace.

    object -> {http://www.loc.gov/audioMD}object

    :tag: Tag name as string
    :returns: Prefixed tag

    """
    if prefix:
        tag = tag[0].upper() + tag[1:]
        return '{%s}%s%s' % (AudioMD_NS, prefix, tag)
    return '{%s}%s' % (AudioMD_NS, tag)


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
    return ET.Element(audiomd_ns(tag, prefix))


def _subelement(parent, tag, prefix=""):
    """Return subelement for the given parent element. Created element is
    appelded to parent element.

    :parent: Parent element
    :tag: Element tagname
    :prefix: Prefix for the tag
    :returns: Created subelement

    """
    return ET.SubElement(parent, audiomd_ns(tag, prefix))


def _one_simple_element(parent, element, element_name):
    if element:
        amd_element = _subelement(parent, element_name)
        amd_element.text = element


def _simple_elements(parent, elements, element_name):
    if elements:
        for element in elements:
            amd_element = _subelement(parent, element_name)
            amd_element.text = element


def _add_elements(parent, elements):
    if elements:
        for element in elements:
            parent.append(element)


def audiomd(ANALOGDIGITALFLAG='FileDigital', fileData=None,
            physicalData=None, audioInfo=None, calibrationInfo=None):
    """Create audioMD Data Dictionary root element.

    :Schema documentation: https://www.loc.gov/standards/amdvmd/audiovideoMDschemas.html
    :child_elements: Any elements appended to the audioMD dictionary

    Returns the following ElementTree structure::


        <amd:AUDIOMD
            xmlns:amd="http://www.loc.gov/audioMD/"
            xmlns:xsi="http://www.w3.org/2001/xmlschema-instance"
            xsi:schemalocation="http://www.loc.gov/audioMD/"

    """
    audiomd = _element('amd')
    audiomd.set(
        xsi_ns('schemaLocation'),
        'http://www.loc.gov/audioMD/')
    audiomd.set('ANALOGDIGITALFLAG', ANALOGDIGITALFLAG)

    if fileData:
        audiomd.append(fileData)
    if physicalData:
        audiomd.append(physicalData)
    if audioInfo:
        audiomd.append(audioInfo)
    if calibrationInfo:
        audiomd.append(calibrationInfo)

    return audiomd


def amd_fileData(
        audioBlockSize=None, audioDataEncoding=None,
        bitsPerSample=None, byteOrder=None,
        messageDigest=None, Compression=None,
        dataRate=None, dataRateMode=None,
        firstSampleOffset=None, firstValidByteBlock=None,
        formatLocation=None, formatName=None,
        formatNote=None, formatVersion=None,
        lastValidByteBlock=None, numSampleFrames=None,
        samplingFrequency=None, security=None,
        use=None, otherUse=None,
        wordSize=None):
    """Returns AudioMD fileData element

    :Schema documentation: https://www.loc.gov/standards/amdvmd/audiovideoMDschemas.html

    Returns the following ElementTree structure::

        <amd:fileData>
            <amd:audioBlockSize></amd:audioBlockSize>
            <amd:audioDataEncoding></amd:audioDataEncoding>
            <amd:bitsPerSample></amd:bitsPerSample>
            <amd:byteOrder></amd:byteOrder>
            {{ messageDigest elements }}
            {{ Compression elements }}
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

    amd_fileData = _element('fileData')

    _simple_elements(amd_fileData, audioBlockSize, 'audioBlockSize')
    _simple_elements(amd_fileData, audioDataEncoding, 'audioDataEncoding')
    _simple_elements(amd_fileData, bitsPerSample, 'bitsPerSample')
    _simple_elements(amd_fileData, byteOrder, 'byteOrder')
    _add_elements(amd_fileData, messageDigest)
    _add_elements(amd_fileData, Compression)
    _simple_elements(amd_fileData, dataRate, 'dataRate')
    _simple_elements(amd_fileData, dataRateMode, 'dataRateMode')
    _simple_elements(amd_fileData, firstSampleOffset, 'firstSampleOffset')
    _simple_elements(amd_fileData, firstValidByteBlock, 'firstValidByteBlock')
    _simple_elements(amd_fileData, formatLocation, 'formatLocation')
    _simple_elements(amd_fileData, formatName, 'formatName')
    _simple_elements(amd_fileData, formatNote, 'formatNote')
    _simple_elements(amd_fileData, formatVersion, 'formatVersion')
    _simple_elements(amd_fileData, lastValidByteBlock, 'lastValidByteBlock')
    _simple_elements(amd_fileData, numSampleFrames, 'numSampleFrames')
    _simple_elements(amd_fileData, samplingFrequency, 'samplingFrequency')
    _simple_elements(amd_fileData, security, 'security')
    _simple_elements(amd_fileData, use, 'use')
    # if 'Other' in use_elements:
    _simple_elements(amd_fileData, otherUse, 'otherUse')
    _simple_elements(amd_fileData, wordSize, 'wordSize')

    return amd_fileData


def amd_messageDigest(messageDigestDatetime, messageDigestAlgorithm,
                    messageDigest):
    """Returns AudioMD messageDigest element

    :Schema documentation: https://www.loc.gov/standards/amdvmd/audiovideoMDschemas.html

    Returns the following ElementTree structure::

        <amd:messageDigest>
            <amd:messageDigestDatetime></amd:messageDigestDatetime>
            <amd:messageDigestAlgorithm></amd:messageDigestAlgorithm>
            <amd:messageDigest></amd:messageDigest>
        </amd:messageDigest>

    """
    amd_messageDigest = _element('messageDigest')

    amd_messageDigestDatetime = _subelement(amd_messageDigest, 'messageDigestDatetime')
    amd_messageDigestDatetime.text = messageDigestDatetime

    amd_messageDigestAlgorithm = _subelement(amd_messageDigest, 'messageDigestAlgorithm')
    amd_messageDigestAlgorithm.text = messageDigestAlgorithm

    amd_messageDigestValue = _subelement(amd_messageDigest, 'messageDigest')
    amd_messageDigestValue.text = messageDigest


    return amd_messageDigest


def amd_compression(codecCreatorApp=None, codecCreatorAppVersion=None,
                    codecName=None, codecQuality=None):
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
    amd_compression = _element('compression')

    _one_simple_element(amd_compression, codecCreatorApp, 'codecCreatorApp')
    _one_simple_element(amd_compression, codecCreatorAppVersion, 'codecCreatorAppVersion')
    _one_simple_element(amd_compression, codecName, 'codecName')
    _one_simple_element(amd_compression, codecQuality, 'codecQuality')

    return amd_compression


def amd_physicalData(EBUStorageMediaCodes=None, condition=None,
                     dimensions=None, disposition=None,
                     equalization=None, generation=None,
                     groove=None, material=None,
                     noiseReduction=None, physFormat=None,
                     speed=None, speedAdjustment=None,
                     speedNote=None, trackFormat=None,
                     tracking=None, note=None):
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
    amd_physicalData = _element('physicalData')

    _simple_elements(amd_physicalData, EBUStorageMediaCodes, 'EBUStorageMediaCodes')
    _simple_elements(amd_physicalData, condition, 'condition')
    _add_elements(amd_fileData, dimensions)
    _simple_elements(amd_physicalData, disposition, 'disposition')
    _simple_elements(amd_physicalData, equalization, 'equalization')
    _simple_elements(amd_physicalData, generation, 'generation')
    _simple_elements(amd_physicalData, groove, 'groove')
    _add_elements(amd_fileData, material)
    _simple_elements(amd_physicalData, noiseReduction, 'noiseReduction')
    _simple_elements(amd_physicalData, physFormat, 'physFormat')
    _simple_elements(amd_physicalData, speed, 'speed')
    _simple_elements(amd_physicalData, speedAdjustment, 'speedAdjustment')
    _simple_elements(amd_physicalData, speedNote, 'speedNote')
    _simple_elements(amd_physicalData, trackFormat, 'trackFormat')
    _add_elements(amd_fileData, tracking)
    _simple_elements(amd_physicalData, note, 'note')

    return amd_physicalData


def amd_dimensions(depth=None, diameter=None, gauge=None, height=None
                   , length=None, note=None, thickness=None, units=None
                   , width=None):
    """Returns AudioMD dimensions element

    :Schema documentation: https://www.loc.gov/standards/amdvmd/audiovideoMDschemas.html

    Returns the following ElementTree structure::

        <amd:dimensions DEPTH="" DIAMETER="" GAUGE="" HEIGHT="" LENGTH=""
            NOTE="" THICKNESS="" UNITS="" WIDTH="">
        </amd:dimensions>

    """

    amd_dimensions = _element('dimensions')

    if depth:
        amd_dimensions.set('DEPTH', depth)
    if diameter:
        amd_dimensions.set('DIAMETER', diameter)
    if gauge:
        amd_dimensions.set('GAUGE', gauge)
    if height:
        amd_dimensions.set('HEIGHT', height)
    if length:
        amd_dimensions.set('LENGTH', length)
    if note:
        amd_dimensions.set('NOTE', note)
    if thickness:
        amd_dimensions.set('THICKNESS', thickness)
    if units:
        amd_dimensions.set('UNITS', units)
    if width:
        amd_dimensions.set('WIDTH', width)

    return amd_dimensions


def amd_material(baseMaterial=None, binder=None, discSurface=None, 
                 oxide=None, activeLayer=None, reflectiveLayer=None, 
                 stockBrand=None, method=None, usedSides=None):
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
    amd_material = _element('material')

    _one_simple_element(amd_material, baseMaterial, 'baseMaterial')
    _one_simple_element(amd_material, binder, 'binder')
    _one_simple_element(amd_material, discSurface, 'discSurface')
    _one_simple_element(amd_material, oxide, 'oxide')
    _one_simple_element(amd_material, activeLayer, 'activeLayer')
    _one_simple_element(amd_material, reflectiveLayer, 'reflectiveLayer')
    _one_simple_element(amd_material, stockBrand, 'stockBrand')
    _one_simple_element(amd_material, method, 'method')
    _one_simple_element(amd_material, usedSides, 'usedSides')

    return amd_material


def amd_tracking(trackingType=None, trackingValue=None):
    """Returns AudioMD tracking element

    :Schema documentation: https://www.loc.gov/standards/amdvmd/audiovideoMDschemas.html

    Returns the following ElementTree structure::

        <amd:tracking>
            <amd:trackingType></amd:trackingType>
            <amd:trackingValue></amd:trackingValue>
        </amd:tracking>

    """
    amd_tracking = _element('tracking')

    _one_simple_element(amd_tracking, trackingType, 'trackingType')
    _one_simple_element(amd_tracking, trackingValue, 'trackingValue')

    return amd_tracking


def amd_audioInfo(duration=None, note=None, numChannels=None,
                  soundChannelMap=None, soundField=None):
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
    amd_audioInfo = _element('audioInfo')

    _simple_elements(amd_audioInfo, duration, 'duration')
    _simple_elements(amd_audioInfo, note, 'note')
    _simple_elements(amd_audioInfo, numChannels, 'numChannels')
    _add_elements(amd_audioInfo, soundChannelMap)
    _simple_elements(amd_audioInfo, soundField, 'soundField')

    return amd_audioInfo


def amd_soundChannelMap(channelnum=None, maplocation=None):
    """Returns soundChannelMap dimensions element

    :Schema documentation: https://www.loc.gov/standards/amdvmd/audiovideoMDschemas.html

    Returns the following ElementTree structure::

        <amd:soundChannelMap>
            <amd:channelAssignment CHANNELNUM="" MAPLOCATION="">
            </amd:channelAssignment>
        <amd:soundChannelMap>

    """

    amd_soundChannelMap = _element('soundChannelMap')
    amd_channelAssignment = _subelement(amd_soundChannelMap, 'channelAssignment')

    if channelnum:
        amd_channelAssignment.set('CHANNELNUM', channelnum)
    if maplocation:
        amd_channelAssignment.set('MAPLOCATION', maplocation)

    return amd_soundChannelMap


def amd_calibrationInfo(calibrationExtInt=None, calibrationLocation=None,
                        calibrationTimeStamp=None, calibrationTrackType=None):
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
    amd_calibrationInfo = _element('calibrationInfo')

    _one_simple_element(amd_calibrationInfo, calibrationExtInt, 'calibrationExtInt')
    _one_simple_element(amd_calibrationInfo, calibrationLocation, 'calibrationLocation')
    _simple_elements(amd_audioInfo, calibrationTimeStamp, 'calibrationTimeStamp')
    _one_simple_element(amd_calibrationInfo, calibrationTrackType, 'calibrationTrackType')

    return amd_calibrationInfo
