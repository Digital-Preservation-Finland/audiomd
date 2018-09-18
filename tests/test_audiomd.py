import audiomd.audiomd as amd
import pytest
import os

NAMESPACES = {'amd': amd.AudioMD_NS}


def test_audiomd_ok():

    compression = amd.amd_compression(codecCreatorApp='SoundForge',
                                      codecCreatorAppVersion='10',
                                      codecName='(:unap)',
                                      codecQuality='lossy')

    file_data = amd.amd_fileData(audioDataEncoding=['PCM'],
                                 bitsPerSample=['8'],
                                 Compression=[compression],
                                 dataRate=['256'],
                                 dataRateMode=['Fixed'],
                                 samplingFrequency=['44.1'])

    audio_info = amd.amd_audioInfo(duration=['PT1H30M'],
                                   numChannels=['1'])

    audiomd = amd.audiomd(fileData=file_data, audioInfo=audio_info)

    assert len(audiomd.xpath(
        "/amd:amd[@ANALOGDIGITALFLAG='FileDigital']", namespaces=NAMESPACES)) == 1
    assert audiomd.xpath("/amd:amd/amd:fileData/amd:audioDataEncoding",
                         namespaces=NAMESPACES)[0].text == 'PCM'
    assert audiomd.xpath("/amd:amd/amd:fileData/amd:bitsPerSample",
                         namespaces=NAMESPACES)[0].text == '8'
    assert audiomd.xpath("/amd:amd/amd:fileData/amd:compression/amd:codecCreatorApp",
                         namespaces=NAMESPACES)[0].text == 'SoundForge'
    assert audiomd.xpath("/amd:amd/amd:fileData/amd:compression/amd:codecCreatorAppVersion",
                         namespaces=NAMESPACES)[0].text == '10'
    assert audiomd.xpath("/amd:amd/amd:fileData/amd:compression/amd:codecName",
                         namespaces=NAMESPACES)[0].text == '(:unap)'
    assert audiomd.xpath("/amd:amd/amd:fileData/amd:compression/amd:codecQuality",
                         namespaces=NAMESPACES)[0].text == 'lossy'
    assert audiomd.xpath("/amd:amd/amd:fileData/amd:dataRate",
                         namespaces=NAMESPACES)[0].text == '256'
    assert audiomd.xpath("/amd:amd/amd:fileData/amd:dataRateMode",
                         namespaces=NAMESPACES)[0].text == 'Fixed'
    assert audiomd.xpath("/amd:amd/amd:fileData/amd:samplingFrequency",
                         namespaces=NAMESPACES)[0].text == '44.1'
    assert audiomd.xpath("/amd:amd/amd:audioInfo/amd:duration",
                         namespaces=NAMESPACES)[0].text == 'PT1H30M'
    assert audiomd.xpath("/amd:amd/amd:audioInfo/amd:numChannels",
                         namespaces=NAMESPACES)[0].text == '1'
