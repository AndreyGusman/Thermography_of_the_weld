#if !defined(__COLOR_PALLETE_CTRL__)
#define __COLOR_PALLETE_CTRL__

#if _MSC_VER > 1000
#pragma once
#endif // _MSC_VER > 1000
// GradientCtrl.h : header file
//

#include "colorpallete.h"

#define GCW_AUTO -1

#define GC_SELCHANGE			1
#define GC_PEGMOVE				2
#define GC_PEGMOVED				3
#define GC_PEGREMOVED			4
#define GC_CREATEPEG			5
#define GC_EDITPEG				6
#define GC_CHANGE				7

#define GC_SELCOUPLECHANGE		8
#define GC_COUPLEPEGMOVE		9
#define GC_CREATECOUPLEPEG		10
#define GC_PEGCOUPLEREMOVED		11


//Ruler Window Style
#define RWSTYLE_VERT          0x0001
#define RWSTYLE_HORZ          0x0002
#define RWSTYLE_LEFTALIGN     0x0004
#define RWSTYLE_RIGHTALIGN    0x0008
#define RWSTYLE_TOPALIGN      RWSTYLE_LEFTALIGN
#define RWSTYLE_BOTTOMALIGN   RWSTYLE_RIGHTALIGN
#define RWSTYLE_DRAWMODAL     0x0010
#define RWSTYLE_DRAWEDGE      0x0020   



struct PegNMHDR
{
	NMHDR nmhdr;
	CPeg peg;
	CCouplePeg pegc;
	int index;
};

struct PegCreateNMHDR
{
	NMHDR nmhdr;
	float position;
	COLORREF colour;
};

class CColorPalleteCtrl;

class CColorPalleteCtrlImpl  
{
public:
	CColorPalleteCtrlImpl(CColorPalleteCtrl *owner);
protected:
	virtual ~CColorPalleteCtrlImpl();

	void Draw(CDC *dc,bool enable,bool showruler);
	void DrawGradient(CDC *dc);
	void DrawPegs(CDC *dc);
	void DrawSelPeg(CDC *dc, int peg);
	void DrawSelPeg(CDC *dc, CPoint point, int direction);
	void DrawSelPegC(CDC *dc, CPoint point, int direction);
	void DrawPeg(CDC *dc, CPoint point, COLORREF colour, int direction);
	void DrawPegC(CDC *dc, CPoint point, COLORREF colour, int direction);
	void DrawEndPegs(CDC *dc);
	
	void DrawRuler(CDC *dc,int wid);
	BOOL DrawVRuler(CDC *pDC, CRect rectRuler); 
	BOOL DrawHRuler(CDC *pDC, CRect rectRuler);
	
	int PointFromPos(float pos);
	float PosFromPoint(int point);
	int GetPegIndent(int index);
	int PtInPeg(CPoint point);

	void GetPegRect(int index, CRect *rect);
	
	void ParseToolTipLine(CString &tiptext, CPeg peg);
	void ShowTooltip(CPoint point, CString text);
	CString ExtractLine(CString source, int line);
	void SetTooltipText(CString text);
	void DestroyTooltip();
	void SynchronizeTooltips();

	bool IsVertical();
	int GetDrawWidth();

	HWND m_wndToolTip;
	TOOLINFO m_ToolInfo;
	CColorPalleteCtrl *m_Owner;
	CToolTipCtrl m_ToolTipCtrl;
	int m_RectCount;
//	BOOL m_LeftDownSide, m_RightUpSide;

	CPeg m_Null;
	CCouplePeg m_coupleNull; 

	COLORREF  m_clrMilimeterLineColor;
	COLORREF  m_clrTextColor;
	UINT      m_nSeperateSize;
	DWORD     m_dwStyle;
	UINT      m_nRulerMargin;
	UINT      m_nDefaultMarginNUM; 

	
	long      m_lScrolPos;
	
	DWORD    GetStyle() { return m_dwStyle; }
	UINT     GetMargin() { return m_nRulerMargin; }

	BOOL SetStartSeperateSize( UINT nSize ) { 
	  m_nSeperateSize = nSize; 
	  return TRUE;
	}
	BOOL	SetMargin( UINT nMargin ) { 
	  m_nDefaultMarginNUM = nMargin;  //NOT m_nRulerMargin
	  return TRUE;
	}
	
	void GetCouplePegRect(int index, CRect *rect, bool isup);
	int  PtInCouplePeg(CPoint point,bool *isup);
	void DrawCouplePegs(CDC *dc)	;
	void DrawSelCouplePeg(CDC *dc, int pegC,bool isup);
	
	float  m_maxvalue;
	float  m_minvalue; 
	int    m_fontsize;

	friend class CColorPalleteCtrl;
};

/////////////////////////////////////////////////////////////////////////////
// CColorPalleteCtrl window

class AFX_CLASS_EXPORT CColorPalleteCtrl : public CWnd
{
// Construction
public:
	CColorPalleteCtrl();
	BOOL Create(const RECT& rect, CWnd* pParentWnd, UINT nID);
	
	enum Orientation
	{
		ForceHorizontal,
		ForceVertical,
		Auto
	};

// Attributes
public:
	int GetGradientWidth() const {return m_Width;};
	void SetGradientWidth(int iWidth) {m_Width = iWidth;};  //ASSERT(iWidth < -1); 
	int GetSelIndex() const {return m_Selected;};
	int SetSelIndex(int iSel);
	int SetSelCoupleIndex(int iSel,bool isup);  //add yzw 
	int GetSelCoupleIndex() const {return m_CoupleSelected;};
	void SetFontSize(int size){ if(m_Impl)m_Impl->m_fontsize = size; }

	const CPeg GetSelPeg() const;
	CColorPalleteDataMgr& GetDataMgr() {return m_DataMgr;};
	void SetGradient(CColorPalleteDataMgr src) {m_DataMgr = src;};
	void ShowTooltips(BOOL bShow = true);
	Orientation GetOrientation() const {return m_Orientation;};
	void SetOrientation(Orientation orientation) {m_Orientation = orientation;};

	void SetTooltipFormat(const CString format);
	CString GetTooltipFormat() const;

//YZW 
	int MoveSelectedCouple(float newpos, BOOL bUpdate); //?
	const CCouplePeg GetSelCouplePeg(bool *isup) const;
	COLORREF SetColourSelectedCouple(COLORREF crNewColour, BOOL bUpdate=TRUE);
	int SetMethodSelectedCouple(InterpolationMethod newMethod, BOOL bUpdate=TRUE);

	void SetRulerMaxValue(float max){if(m_Impl)m_Impl->m_maxvalue = max;};
	void SetRulerMinValue(float min){if(m_Impl)m_Impl->m_minvalue = min;};

	void SetCtrlEnable(bool bEnable){m_bEnable=bEnable;};  //设置是否可以交互  
	void SetShowRuler(bool bShow){ m_bShowRuler= bShow;};  //是否显示 RULER  
	void SetRulerStepNum(UINT input){ if(m_Impl) m_Impl->SetMargin(input); }

// Operations
public:
	void DeleteSelected(BOOL bUpdate);
	int MoveSelected(float newpos, BOOL bUpdate);
	COLORREF SetColourSelected(COLORREF crNewColour, BOOL bUpdate);

// Internals
protected:
	BOOL RegisterWindowClass();

	void GetPegRgn(CRgn *rgn);
	void GetPegCoupleRgn(CRgn *rgn);

	void SendBasicNotification(UINT code, CPeg peg, int index);

	CColorPalleteDataMgr m_DataMgr;
	int m_Width;

	int m_Selected;
	int m_LastPos;
	CPoint m_MouseDown;

	int  m_CoupleSelected;  // 
	bool m_CoupleUp;

	BOOL m_bShowToolTip;
	CString m_ToolTipFormat;

	enum Orientation m_Orientation;

	CColorPalleteCtrlImpl *m_Impl;

	friend class CColorPalleteCtrlImpl;
	
	bool m_bEnable;  // 没有交互， 没有尺度显示，
	bool m_bShowRuler; // 刻度是否显示 

	
// Overrides
	// ClassWizard generated virtual function overrides
	//{{AFX_VIRTUAL(CColorPalleteCtrl)
	public:
	virtual BOOL PreTranslateMessage(MSG* pMsg);
	protected:
	virtual void PreSubclassWindow();
	//}}AFX_VIRTUAL

// Implementation
public:
	virtual ~CColorPalleteCtrl();

	// Generated message map functions
protected:

	//{{AFX_MSG(CColorPalleteCtrl)
	afx_msg void OnPaint();
	afx_msg BOOL OnEraseBkgnd(CDC* pDC);

	afx_msg void OnLButtonDown(UINT nFlags, CPoint point);
	afx_msg void OnMouseMove(UINT nFlags, CPoint point);
	afx_msg void OnLButtonUp(UINT nFlags, CPoint point);
	afx_msg void OnKeyDown(UINT nChar, UINT nRepCnt, UINT nFlags);
	afx_msg void OnLButtonDblClk(UINT nFlags, CPoint point);

	afx_msg UINT OnGetDlgCode();
	afx_msg void OnKillFocus(CWnd* pNewWnd);
	//}}AFX_MSG
	DECLARE_MESSAGE_MAP()
	

};

/////////////////////////////////////////////////////////////////////////////

//{{AFX_INSERT_LOCATION}}
// Microsoft Visual C++ will insert additional declarations immediately before the previous line.

#endif 



	// 添加几种模式， 1  不能调整的，不响应人和状态  2 能投响应对应的温度状态，
	//					 不显示 控制点，等温带控制点 不能调节，  
	//					 不 显示温度信息， 温度 信息的准确性 
	//            显示和不显示   温度状态的 最高 和最低值，
	
	// 显示 改为 非小数类型  256 级别的   TIP 也一样 

	// 每次移动了界面要处理 重新 处理调色板 
	
	// 添加对比调色板， 让图像显示出来，进行处理   void CFireWnd::CreateBitmap()  进行对比，处理好的调色板信息  生成工具，  ？？？？？？