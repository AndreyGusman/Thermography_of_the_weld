///////////////////////////////////////////////////////////////


#if !defined(AFX_SKINDIALOG_H__6206972E_1F54_11D4_8166_D172E91C6E8C__INCLUDED_)
#define AFX_SKINDIALOG_H__6206972E_1F54_11D4_8166_D172E91C6E8C__INCLUDED_

#if _MSC_VER > 1000
#pragma once
#endif // _MSC_VER > 1000

#ifndef __AFXTEMPL_H__
#include <afxtempl.h>
#endif

#include "BitmapBtn.h"

/////////////////////////////////////////////////////////////////////////////
// CSkinDialog dialog

class AFX_CLASS_EXPORT  CSkinDialog : public CDialog
{
protected:
	CTypedPtrArray<CPtrArray, CSkinButton*> m_Buttons;
	CTypedPtrArray<CPtrArray, CSkinSlider*> m_Sliders;
	CTypedPtrArray<CPtrArray, CSkinLabel*> m_Labels;
	CTypedPtrArray<CPtrArray, CSkinProgress*> m_Progress;
	CRgn *m_Rgn;
	void AssignValues();
// Construction
public:
	void SetButtonToolTip(CString m_IDName, CString m_NewToolTip);
	void SetTextToolTip(CString m_IDName, CString m_NewToolTip);
	void SetProgressToolTip(CString m_IDName, CString m_NewToolTip);
	void SetMoveAble(bool bMove);

	virtual void ProgresChanged(CString m_Name);
	void SetProgressPos(CString m_ID, int m_newPos);
	int GetProgressPos(CString m_ID);
	void ChangeProgress(int m_ID);
	void SetButtonCheck(CString m_IDName, BOOL m_NewValue);
	BOOL GetButtonCheck(CString m_IDName);
	void SetButtonEnable(CString m_IDName, BOOL m_Enable);
	int GetTrackBarPos(CString m_IDName);
	CString GetDisplayText(CString m_IDName);
	void SetText(CString m_ID, CString m_newText);
	void SetTrackBarPos(CString m_ID, int m_newPos);
	void ReadTrackBarInfo(CIniFile m_File);
	void ReadProgressInfo(CIniFile m_File);
	CRgn* GetRGN();
	void SetMenuID(UINT mMenuID);
	void SetSkinFile(char* mSkinName);
	CSkinDialog();   // standard constructor
	CSkinDialog(UINT nIDTemplate, CWnd* pParentWnd = NULL);
	CSkinDialog(LPCTSTR lpszTemplateName, CWnd* pParentWnd = NULL);
	~CSkinDialog();
	
	virtual void ButtonPressed(CString m_ButtonName);
	virtual void PressButton(int m_ID);

	virtual void TrackChange(CString m_ButtonName, UINT nSBCode, UINT nPos);
	virtual void ChangeTrack(int m_ID, UINT nSBCode, UINT nPos);

	virtual void TextClicked(CString m_TextName);
	virtual void ClickText(int m_ID);
	virtual void MouseMoved(CString m_ButtonName, int x, int y);
// Dialog Data
	//{{AFX_DATA(CSkinDialog)
		// NOTE: the ClassWizard will add data members here
	//}}AFX_DATA


// Overrides
	// ClassWizard generated virtual function overrides
	//{{AFX_VIRTUAL(CSkinDialog)
	//}}AFX_VIRTUAL

// Implementation
protected:
	void ReadTextInfo(CIniFile m_File);
	void ReadButtonInfo(CIniFile m_File);
	void LoadBitmap(const char* szFilename, CBitmap* pBitmap);
	CString m_SkinName;
	virtual void Setup(CBitmap& mBitmap);
	UINT m_MenuID;
	bool bMoveable;
	CBitmap m_Normal, m_Over, m_Down, m_Disabled;

	// change 2006-4-15
	LPPICTURE	gDLG_Picture_Normal, 
				gDLG_Picture_Mask,
				gDLG_Picture_Over,
				gDLG_Picture_Down,
				gDLG_Picture_Disabled;

	virtual void LoadSkins(); //LPCTSTR mNormal, LPCTSTR mOver, LPCTSTR mDown, LPCTSTR mDisabled);
	void Free();
	

	// Generated message map functions
	//{{AFX_MSG(CSkinDialog)
	afx_msg void OnPaint();
	afx_msg void OnLButtonDown(UINT nFlags, CPoint point);
	virtual BOOL OnInitDialog();
	afx_msg void OnRButtonDown(UINT nFlags, CPoint point);
	afx_msg void OnMouseMove(UINT nFlags, CPoint point);
	//}}AFX_MSG
	DECLARE_MESSAGE_MAP()

public:

//	void OnPaint();
//	void OnLButtonDown(UINT nFlags, CPoint point);
//	virtual BOOL OnInitDialog();
//	void OnRButtonDown(UINT nFlags, CPoint point);
//	void OnMouseMove(UINT nFlags, CPoint point);

};


//{{AFX_INSERT_LOCATION}}
// Microsoft Visual C++ will insert additional declarations immediately before the previous line.

#endif // !defined(AFX_SKINDIALOG_H__6206972E_1F54_11D4_8166_D172E91C6E8C__INCLUDED_)
