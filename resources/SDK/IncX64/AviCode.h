// Bmp2Avi.h: interface for the CAviCode class.
//
//////////////////////////////////////////////////////////////////////

#if !defined(AFX_BMP2AVI_H__7CE8DA87_D00C_4C2A_8AE8_F5A82582CE1A__INCLUDED_)
#define AFX_BMP2AVI_H__7CE8DA87_D00C_4C2A_8AE8_F5A82582CE1A__INCLUDED_

#if _MSC_VER > 1000
#pragma once
#endif // _MSC_VER > 1000

#include <vfw.h>
#include <afxmt.h>



// move to userdef.h 

class DLLPORT CAviCode  
{
public:
	BOOL IsRecording() const {return m_bIsRecording;};
	BOOL PushFrame(const BYTE * pData, int intBufferSize, const BITMAPINFO *pInfo);
	void CloseAviFile();
	BOOL CreateAviFile(HWND hwndParent, UINT fps, char *avipathfile, const BITMAPINFO * pInfo);
	UINT GetFrameCounter() const {return m_intFrameCounter;};
	CAviCode();
	virtual ~CAviCode();

private:
	CCriticalSection m_cs;//多线程保护
	UINT m_intFrameCounter;
	BOOL m_bIsRecording;
	PAVISTREAM m_psavi;
	PAVISTREAM m_psCompressed;
	PAVIFILE m_pfile;

	BOOL m_bIsGray256;//256色图像标识
	BOOL m_bIsXvidReady;//是否安装了Xvid编码器
};

#endif // !defined(AFX_BMP2AVI_H__7CE8DA87_D00C_4C2A_8AE8_F5A82582CE1A__INCLUDED_)
