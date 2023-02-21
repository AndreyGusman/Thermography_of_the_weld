#ifndef   _Y_SKIN_DIALOG_
#define   _Y_SKIN_DIALOG_

//
#include <afxwin.h>
#include <afxcmn.h>
#include <afxext.h>         // MFC extensions
#include <afxdisp.h>        // MFC Automation classes
#include <afxdtctl.h>		// MFC support for Internet Explorer 4 Common Controls
#include <io.h>

/////////////////////////////////////////////////////////////////////////////
// CBitmapBtn window

class  CBitmapBtn : public CButton
{
	void InitToolTip();
	CToolTipCtrl m_ToolTip;
// Construction
public:
	BOOL m_Check, m_CheckedButton;
	CBitmapBtn();
	void SetTooltipText(CString* spText, BOOL bActivate = TRUE);
	void ActivateTooltip(BOOL bEnable = TRUE);

// Overrides
	// ClassWizard generated virtual function overrides
	//{{AFX_VIRTUAL(CBitmapBtn)
	public:
	virtual BOOL PreTranslateMessage(MSG* pMsg);
	protected:
	virtual void PreSubclassWindow();
	//}}AFX_VIRTUAL

// Implementation
public:
	void SetCheck(BOOL m_NewValue);
	void SetBitmap(CBitmap& mNrml, CBitmap& mOvr, CBitmap& mDwn, CBitmap& mDsbl);
	virtual ~CBitmapBtn();

	// Generated message map functions
protected:
	BOOL m_MouseOnButton;
	CBitmap m_Normal, m_Over, m_Down, m_Disabled;
	virtual void DrawItem(LPDRAWITEMSTRUCT lpDrawItemStruct);
	//{{AFX_MSG(CBitmapBtn)
	afx_msg void OnKillFocus(CWnd* pNewWnd);
	afx_msg void OnMouseMove(UINT nFlags, CPoint point);
	afx_msg void OnCaptureChanged(CWnd *pWnd);
	afx_msg BOOL OnEraseBkgnd(CDC* pDC);
	//}}AFX_MSG

	DECLARE_MESSAGE_MAP()
};

/////////////////////////////////////////////////////////////////////////////


#include <afxwin.h>
#include <afxcmn.h>
#include "BitmapBtn.H"

/////////////////////////////////////////////////////////////////////////////
// CAnimatedLabel window

class CAnimatedLabel : public CBitmapBtn //CStatic
{
	int m_Strpos, m_MaxText;
	CString m_Label;
// Construction
public:
	CAnimatedLabel();

// Attributes
public:

// Operations
public:

// Overrides
	// ClassWizard generated virtual function overrides
	//{{AFX_VIRTUAL(CAnimatedLabel)
	//}}AFX_VIRTUAL

// Implementation
public:
	COLORREF m_TextColor;
	void SetBitmap(CBitmap& mBack);
	void SetFont(CFont& mNewFont);
	void SetText(CString mNewText);
	virtual ~CAnimatedLabel();

	// Generated message map functions
protected:
	CBitmap m_Back;
	void UpdateTimer();
	BOOL m_Timered;
	CFont m_Font;
	//{{AFX_MSG(CAnimatedLabel)
	afx_msg void OnTimer(UINT nIDEvent);
	afx_msg void OnPaint();
	//}}AFX_MSG

	DECLARE_MESSAGE_MAP()
};


/////////////////////////////////////////////////////////////////////////////
// CBitmapProgress window

class CBitmapProgress : public CBitmapBtn
{
// Construction
public:
	BOOL m_Horizantal;
	CBitmapProgress();
	void SetBitmap(CBitmap& mZero, CBitmap& mFull);
// Attributes
public:

// Operations
public:

// Overrides
	// ClassWizard generated virtual function overrides
	//{{AFX_VIRTUAL(CBitmapProgress)
	//}}AFX_VIRTUAL

// Implementation
public:
	virtual ~CBitmapProgress();
	UINT GetPos() { return m_Pos; }
	void SetPos(UINT m_newPos);
	// Generated message map functions
protected:
	BOOL m_MouseOnProgress;
	//{{AFX_MSG(CBitmapProgress)
	afx_msg BOOL OnEraseBkgnd(CDC* pDC);
	afx_msg void OnPaint();
	afx_msg void OnLButtonDown(UINT nFlags, CPoint point);
	afx_msg void OnLButtonUp(UINT nFlags, CPoint point);
	afx_msg void OnMouseMove(UINT nFlags, CPoint point);
	//}}AFX_MSG

	DECLARE_MESSAGE_MAP()
private:
	UINT m_Pos;
};


/////////////////////////////////////////////////////////////////////////////
// CBitmapSlider window

class CBitmapSlider : public CSliderCtrl
{
protected:
	CBitmap m_Back, m_ThumbNormal, m_ThumbDown;
	// change 2006-4-15
	LPPICTURE gpPicture_Normal, gpPicture_Down;

// Construction
public:
	CBitmapSlider();

// Attributes
public:

// Operations
public:

// Overrides
	// ClassWizard generated virtual function overrides
	//{{AFX_VIRTUAL(CBitmapSlider)
	//}}AFX_VIRTUAL

// Implementation
public:
	void SetBitmap(CBitmap& mBack, CBitmap& mTNormal, CBitmap& mTDown);
	virtual ~CBitmapSlider();

	// Generated message map functions
protected:
	void getThumbRect(CRect& r);
	BOOL m_MouseOnThumb;
	//{{AFX_MSG(CBitmapSlider)
	afx_msg void OnPaint();
	afx_msg void OnLButtonDown(UINT nFlags, CPoint point);
	afx_msg void OnLButtonUp(UINT nFlags, CPoint point);
	afx_msg void OnMouseMove(UINT nFlags, CPoint point);
	afx_msg void OnCaptureChanged(CWnd *pWnd);
	afx_msg BOOL OnEraseBkgnd(CDC* pDC);
	//}}AFX_MSG

	DECLARE_MESSAGE_MAP()
};

/////////////////////////////////////////////////////////////////////////////
// CSkinButton window

class CSkinButton : public CBitmapBtn
{
// Construction
public:
// Attributes
	CString m_IDName;
	int m_ID;
public:

// Operations
public:

// Overrides
	// ClassWizard generated virtual function overrides
	//{{AFX_VIRTUAL(CSkinButton)
	//}}AFX_VIRTUAL

// Implementation
public:
	void CopyFrom(CRect r, CBitmap& m_N, CBitmap& m_O, CBitmap& m_Dw, CBitmap& m_Ds);

	// Generated message map functions
protected:
	//{{AFX_MSG(CSkinButton)
	afx_msg void OnLButtonUp(UINT nFlags, CPoint point);
	afx_msg void OnMouseMove(UINT nFlags, CPoint point);
	//}}AFX_MSG

	DECLARE_MESSAGE_MAP()
};

class CSkinLabel : public CAnimatedLabel
{
// Construction
public:
	CString m_IDName;
	int m_ID;

// Attributes
public:

// Operations
public:

// Overrides
	// ClassWizard generated virtual function overrides
	//{{AFX_VIRTUAL(CSkinLabel)
	//}}AFX_VIRTUAL

// Implementation
public:
	void CopyFrom(CRect r, CBitmap& m_B);
	// Generated message map functions
protected:
	//{{AFX_MSG(CSkinLabel)
	afx_msg void OnLButtonUp(UINT nFlags, CPoint point);
	afx_msg void OnMouseMove(UINT nFlags, CPoint point);
	//}}AFX_MSG

	DECLARE_MESSAGE_MAP()
};

class CSkinProgress : public CBitmapProgress
{
// Construction
public:
	CSkinProgress();

// Attributes
public:
	CString m_IDName;
	int m_ID;

// Operations
public:

// Overrides
	// ClassWizard generated virtual function overrides
	//{{AFX_VIRTUAL(CSkinProgress)
	//}}AFX_VIRTUAL

// Implementation
public:
	void CopyFrom(CRect r, CBitmap& m_N, CBitmap& m_Dw);
	virtual ~CSkinProgress();

	// Generated message map functions
protected:
	//{{AFX_MSG(CSkinProgress)
	afx_msg void OnLButtonUp(UINT nFlags, CPoint point);
	afx_msg void OnMouseMove(UINT nFlags, CPoint point);
	//}}AFX_MSG

	DECLARE_MESSAGE_MAP()
};


class CSkinSlider : public CBitmapSlider
{
// Construction
public:
// Attributes
public:
	CString m_IDName;
	int m_ID;

	void CopyFrom(CRect r, CBitmap& m_N, LPCTSTR m_TN, LPCTSTR m_TD);
// Operations
public:

// Overrides
	// ClassWizard generated virtual function overrides
	//{{AFX_VIRTUAL(CSkinSlider)
	//}}AFX_VIRTUAL

// Implementation
public:
	// Generated message map functions
protected:
	//{{AFX_MSG(CSkinSlider)
	afx_msg void OnHScroll(UINT nSBCode, UINT nPos, CScrollBar* pScrollBar);
	afx_msg void OnVScroll(UINT nSBCode, UINT nPos, CScrollBar* pScrollBar);
	afx_msg void OnLButtonUp(UINT nFlags, CPoint point);
	afx_msg void OnMouseMove(UINT nFlags, CPoint point);
	afx_msg void OnLButtonDown(UINT nFlags, CPoint point);
	//}}AFX_MSG

	DECLARE_MESSAGE_MAP()
private:
	BOOL m_Scrolling;
};




#endif 


//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++//
//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++////++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++//
//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++//
//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++//
//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++//

#ifndef __CINIFILE_H__
#define __CINIFILE_H__


class  CIniFile
{
	CString m_Name;
public:
	CIniFile(CString m_FName);

	CString ReadString(CString m_Sec, CString m_Ident, CString m_Def,char *Buffer,int buffsize);
//	BOOL WriteString(CString m_Sec, CString m_Ident, CString m_Val);
//	BOOL ReadSections(CStringArray& m_Secs);
	BOOL ReadSection(CString m_Sec, CStringArray& m_Secs);
};

#endif