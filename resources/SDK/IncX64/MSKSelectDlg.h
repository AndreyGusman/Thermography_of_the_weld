#if !defined(AFX_MASKSELECT_H__INCLUDED_)
#define AFX_MASKSELECT_H__INCLUDED_

#if _MSC_VER > 1000
#pragma once
#endif // _MSC_VER > 1000

//
//  参考开源工程 实现  2014-6



#include "GHSDKRes.h"


typedef		short						ELETYPE;

#include "api.h"
/////////////////////////////////////////////////////////////////////////////
// CMaskSelectDlg dialog

class DLLPORT CMaskSelectDlg : public CDialog
{
// Construction
public:
	CMaskSelectDlg(void * devicehandle,  CWnd* pParent = NULL);   // standard constructor
	~CMaskSelectDlg();						// standard destructor

	void * m_DeviceHandle; 
	
	short	LTBMP_WIDTH;	//	
	short	LTBMP_HEIGHT;	//
	long	LTBMP_BITCNT;	//
	
	short   DEF_GRAY;		//默认的灰度[白色]
	short	cDefBT	;			//默认的坏点类型
	short	cSCALE	;  // 不做放大 
// Dialog Data
	//{{AFX_DATA(CMaskSelectDlg)
	enum { IDD = IDD_BG_MARK };

	CStatic	m_vzi; // KEY 

	//CString	m_Xpos;
	//CString	m_Ypos;

	//}}AFX_DATA
	CDC*		m_pDcVltMem;
	CBitmap*	m_pBmp;

	BYTE*			m_pbi;				//BITMAPINFO*
	BYTE*			m_ptEngBits;		//放大八倍的位图数据 
	
	//用来校正坏点的局部显示区域
	ELETYPE*		m_pttBmp;			// m_pttBmp  RAW 数据

	BYTE*			m_ptLocBits;		// 全图 是 正常上下关系 


	CPoint			m_PreMp;			//鼠标的上一次的屏幕坐标,<应该记录图象坐标>
	BOOL			m_EnMouseMov;
	short			m_DefBT;			//默认的坏点类型
	BOOL			m_bModFlag;			


	HBRUSH		OnCtlColor(CDC* pDC, CWnd* pWnd, UINT nCtlColor) ; 
	void		PrepareLocImage(CPoint	InImagePos,int MoveType=0);
	void		InitLocImageBuffer(bool clearEng=false,bool clearBadpts=false);
	void		EnlargeBmp8Scale(BYTE* pSrc,BYTE* pNew,int OriImgWidth,int OriImgHeight,int nScale,int EnlargeType=0);

	void		UpdateImageData(CPoint realPt,BOOL bForceUpdate=FALSE,BOOL bUpdateData=FALSE);
	void		UpdateDisp(CPoint realPt);
	void		DrawEnlagImage();
	void		OnPrepareDC(CDC* pDC,CPrintInfo* pInfo=NULL);
	void		DrawGraph(CDC* pDC,CWnd& wnd,BYTE* pbinfo/*位图信息*/,BYTE* pbits/*位图数据*/);

	void		DrawGrid(CDC* pDC,CWnd& wnd);		//画网格

	CPoint		GetInImagePos(CWnd& srcWnd,CPoint	curScreenPos,BOOL bScreenToImage);


// Overrides
	// ClassWizard generated virtual function overrides
	//{{AFX_VIRTUAL(CMaskSelectDlg)
	public:
	virtual BOOL PreTranslateMessage(MSG* pMsg);
	protected:
	virtual void DoDataExchange(CDataExchange* pDX);    // DDX/DDV support
	//}}AFX_VIRTUAL

private:

	CBrush		m_Pctbr,m_Dlgbr,m_Txtbr;


	CPen   IRpen;
	CBrush IRbrush;
	//网络横向格子个数 横纵 4:3，所以纵向最好
	int				m_GridHorizonWid;	

	//图像校准的窗口客户区坐标
	CPoint			m_AjustPoint[4];
	CPoint          m_AjustPointVL[4]; 

	BYTE*			m_pSelectAreaMark;		
	//BYTE*			m_pSelectAreaMarkBak;//屏蔽块掩码
	///有效区域在图像缓冲区的映射表 0X00 代表无效，0X01 代表有效，0X10 代表背景区
	BYTE*			m_pSelectAreaToImageBuffer; 

	int  m_stBlockX;		//鼠标拖动的起始块x
	int  m_stBlockY;		//鼠标拖动的起始块y
	//	int  m_prevBlockX;		//鼠标前次拖动到的块x
	//	int  m_prevBlockY;		//鼠标前次拖动到的块y
	int  m_curBlockX;		//鼠标本次拖动到的块x
	int  m_curBlockY;		//鼠标本次拖动到的块y
	bool m_bDrag;			//正在进行左键拖选

	//设置屏蔽区分块个数
	bool  SetGridHorizonNum(int wid ,int m_ImageWidth,  int  m_ImageHeight );
	//根据有效区域的整块掩码 ，确定数据区域那些像素有效与无效
	void  SetValidImageBufferMap(int wid ,int hei);
	void  UnPackBufferMap(int wid ,int hei);  //from mask to grid data.  

	int  GetGridHorizonNum()
	{
		return		LTBMP_WIDTH/m_GridHorizonWid  ;
	}
	BYTE* GetGridHide()
	{
		return			m_pSelectAreaMark;
	}


	//5.图像校准 - 与可见光配对
	double			dbTranformMatrix[3][3];
	//从红外图像坐标得到可见光坐标
	void GetVisualCoordinate(double TranformMatrix[3][3],double srcX,double srcY,double& reX,double& reY);//XY.1
	//获得转换矩阵
	bool GetTransformMatrix(POINT IrC[3],POINT VC[3],double TranformMatrix[3][3]);//XY.3
	//3*3矩阵求逆
	bool Matrix3X3_Inverse(double Matrix[3][3],double Matrix_Inv[3][3]);	//XY.4
	//根据定标点获得视频的坐标映射关系,要先求转换矩阵
	bool GetVideoTransform(bool bForce=true);	//XY.2  bForce==true 强制求转换矩阵
	bool			m_bHaveMap;			//已经有映射矩阵


// Implementation
protected:

//	CDemo1View *pView; 
	
	// Generated message map functions
	//{{AFX_MSG(CMaskSelectDlg)
	virtual BOOL OnInitDialog();
	afx_msg void OnPaint();
	afx_msg void OnLButtonDown(UINT nFlags, CPoint point);
	afx_msg void OnMouseMove(UINT nFlags, CPoint point);
	afx_msg void OnLButtonUp(UINT nFlags, CPoint point);
	afx_msg void OnClose();
	afx_msg void OnBtnRdMask();
	afx_msg void OnBtnSaveMask();
	afx_msg void OnBtnClearMask();
	//}}AFX_MSG
	DECLARE_MESSAGE_MAP()
};

//{{AFX_INSERT_LOCATION}}
// Microsoft Visual C++ will insert additional declarations immediately before the previous line.

#endif //
