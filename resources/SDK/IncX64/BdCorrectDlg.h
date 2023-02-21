#if !defined(AFX_BDCORRECTDLG_H__335FDEA3_F6E1_4DE2_93A5_8377A5326664__INCLUDED_)
#define AFX_BDCORRECTDLG_H__335FDEA3_F6E1_4DE2_93A5_8377A5326664__INCLUDED_

#if _MSC_VER > 1000
#pragma once
#endif // _MSC_VER > 1000
// BdCorrectDlg.h : header file
//
//  参考开源工程 实现  2014-6



#include "GHSDKRes.h"


typedef		short						ELETYPE;

#include "api.h"
/////////////////////////////////////////////////////////////////////////////
// CBdCorrectDlg dialog

class DLLPORT CBdCorrectDlg : public CDialog
{
// Construction
public:
	CBdCorrectDlg(GHDEV_HND devicehandle,int stx,int sty,  CWnd* pParent = NULL);   // standard constructor
	~CBdCorrectDlg();						// standard destructor

	GHDEV_HND m_DeviceHandle; 
	int AreaY;
	int AreaX;	
// Dialog Data
	//{{AFX_DATA(CBdCorrectDlg)
	enum { IDD = IDD_BDCORRECT_DIALOG };

	CButton	m_ChkCtl;
	CSpinButtonCtrl	m_SpnCtl;
	CEdit	m_gdkInfo;
	CSliderCtrl	m_sldGDK;

	CStatic	m_vzi; // KEY 
	CStatic	m_gzi;

	CString	m_Xpos;
	CString	m_Ypos;
	CString	m_BpCnt;
	CString	m_pixValue;
	float	m_gdkInfoValue;
	long	m_PlaValue;
	//}}AFX_DATA
	CDC*		m_pDcVltMem;
	CBitmap*	m_pBmp;

	//三幅位图的位图信息一样，所以只定义一个
	BYTE*			m_pbi;				//BITMAPINFO*

	BYTE*			m_ptEngBits;		//放大八倍的位图数据 
	
	//用来校正坏点的局部显示区域
	ELETYPE*		m_pttBmp;			//原始数据 RAW 数据

	BYTE*			m_ptLocBits;		//位图数据[灰度数组]  全图，而且是 正常上下关系 

	short*			m_BadPoints;		//存放坏点类型的数组

	CPoint			m_PreMp;			//鼠标的上一次的屏幕坐标,<应该记录图象坐标>
	BOOL			m_EnMouseMov;
	short			m_DefBT;			//默认的坏点类型
	BOOL			m_bModFlag;			


	HBRUSH		OnCtlColor(CDC* pDC, CWnd* pWnd, UINT nCtlColor) ; 
	void		PrepareLocImage(CPoint	InImagePos,int MoveType=0);
	void		InitLocImageBuffer(bool clearEng=false,bool clearBadpts=false);
	void		EnlargeBmp8Scale(BYTE* pSrc,BYTE* pNew,int OriImgWidth,int OriImgHeight,int nScale,int EnlargeType=0);

	void		UpdateImageData(CPoint realPt,BOOL bForceUpdate=FALSE,BOOL bUpdateData=TRUE);
	void		UpdateDisp(CPoint realPt);
	void		DrawEnlagImage();
	void		OnPrepareDC(CDC* pDC,CPrintInfo* pInfo=NULL);
	void		DrawGraph(CDC* pDC,CWnd& wnd,BYTE* pbinfo/*位图信息*/,BYTE* pbits/*位图数据*/);
	void		DrawGrid(CDC* pDC,CWnd& wnd);		//画网格
	void		DrawBadPoint(CDC* pDC,CWnd& wnd);	//画坏点
	CPoint		GetInImagePos(CWnd& srcWnd,CPoint	curScreenPos,BOOL bScreenToImage);


// Overrides
	// ClassWizard generated virtual function overrides
	//{{AFX_VIRTUAL(CBdCorrectDlg)
	public:
	virtual BOOL PreTranslateMessage(MSG* pMsg);
	protected:
	virtual void DoDataExchange(CDataExchange* pDX);    // DDX/DDV support
	//}}AFX_VIRTUAL

private:

	CBrush		m_Pctbr,m_Dlgbr,m_Txtbr;


// Implementation
protected:

//	CDemo1View *pView; 
	
	// Generated message map functions
	//{{AFX_MSG(CBdCorrectDlg)
	virtual BOOL OnInitDialog();
	afx_msg void OnPaint();
	afx_msg void OnLButtonDown(UINT nFlags, CPoint point);
	afx_msg void OnClose();
	afx_msg void OnBtnbraBps();
	afx_msg void OnBtnsavbp2raw();
	afx_msg void OnBtnclrall();
	//}}AFX_MSG
	DECLARE_MESSAGE_MAP()
};

//{{AFX_INSERT_LOCATION}}
// Microsoft Visual C++ will insert additional declarations immediately before the previous line.

#endif // !defined(AFX_BDCORRECTDLG_H__335FDEA3_F6E1_4DE2_93A5_8377A5326664__INCLUDED_)
