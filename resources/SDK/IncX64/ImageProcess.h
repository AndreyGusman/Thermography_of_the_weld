#pragma once
#include "StdAfx.h"

#include "IRArith.h"
//#include "Api.h"


class CImageProcess
{
public:
	CImageProcess();
	~CImageProcess();
public:
	//IRArith* m_pArith;
	

	LPCTSTR sPath;	

	void init(GHDEV_HND handle);
	void EnableB(bool enable);
	void EnableK(bool enable);
	void ResetB();
	void ResetK();
	void GenY16(short *pOutOri);
	void GenBValue(bool bGenBValue, LPCTSTR sPath, LPCTSTR userfileName);
	void GenKValue(bool bGenKValue, LPCTSTR sPath, LPCTSTR userfileName);
	void ReplaceBadPixel(short*pSrc);

private:
	//IRArith* m_pArith;
	int m_imageX;
	int m_imageY;
	unsigned int m_imageSize;
	GHDEV_HND m_DeviceHandle;

	int m_nucFrameNum;
	short *imgL;
	short AVE_L;
	short *imgLShift;
	short *imgH;
	short *imgK;
	short *imgMark;
	bool isUseB;
	bool isUseK;

	CString sFilePathB;
	CString sFilePathK;

	
	bool setImageType(GHDEV_HND handle, unsigned char type[]);
	void GetRawImage(bool isK_No_B);
	bool SaveRawData(LPCTSTR szFile, int nNum, short * pData);
	bool LoadRawData(LPCTSTR szFile, int nNum, short * pData);

	CString GetKFileNameStr(LPCTSTR strFolderPath, LPCTSTR userfileName, bool isReadPath);
	CString GetBFileNameStr(LPCTSTR strFolderPath, LPCTSTR userfileName, bool isReadPath);
	CString setTempPos(int temp /*10*/, bool isReadPath); //
	CString setIntPos(int integrationTime /*clk*/, bool isReadPath);
	CString setGainPos(int gain);


	//show x16   
	unsigned char  YUANSHI[16] = { 0xFF, 0xFF, 0xAA, 0xFF, 0x00, 0x11, 0x00, 0x00,
		0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00 };
	//show Y16                                 		                                                                                
	unsigned char  Y16[16] = { 0xFF, 0xFF, 0xAA, 0xFF, 0x00, 0x12, 0x00, 0x00,
		0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00 };


};

