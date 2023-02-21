#if !defined(AFX_MASKSELECT_H__INCLUDED_)
#define AFX_MASKSELECT_H__INCLUDED_

#if _MSC_VER > 1000
#pragma once
#endif // _MSC_VER > 1000

//
//  �ο���Դ���� ʵ��  2014-6



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
	
	short   DEF_GRAY;		//Ĭ�ϵĻҶ�[��ɫ]
	short	cDefBT	;			//Ĭ�ϵĻ�������
	short	cSCALE	;  // �����Ŵ� 
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
	BYTE*			m_ptEngBits;		//�Ŵ�˱���λͼ���� 
	
	//����У������ľֲ���ʾ����
	ELETYPE*		m_pttBmp;			// m_pttBmp  RAW ����

	BYTE*			m_ptLocBits;		// ȫͼ �� �������¹�ϵ 


	CPoint			m_PreMp;			//������һ�ε���Ļ����,<Ӧ�ü�¼ͼ������>
	BOOL			m_EnMouseMov;
	short			m_DefBT;			//Ĭ�ϵĻ�������
	BOOL			m_bModFlag;			


	HBRUSH		OnCtlColor(CDC* pDC, CWnd* pWnd, UINT nCtlColor) ; 
	void		PrepareLocImage(CPoint	InImagePos,int MoveType=0);
	void		InitLocImageBuffer(bool clearEng=false,bool clearBadpts=false);
	void		EnlargeBmp8Scale(BYTE* pSrc,BYTE* pNew,int OriImgWidth,int OriImgHeight,int nScale,int EnlargeType=0);

	void		UpdateImageData(CPoint realPt,BOOL bForceUpdate=FALSE,BOOL bUpdateData=FALSE);
	void		UpdateDisp(CPoint realPt);
	void		DrawEnlagImage();
	void		OnPrepareDC(CDC* pDC,CPrintInfo* pInfo=NULL);
	void		DrawGraph(CDC* pDC,CWnd& wnd,BYTE* pbinfo/*λͼ��Ϣ*/,BYTE* pbits/*λͼ����*/);

	void		DrawGrid(CDC* pDC,CWnd& wnd);		//������

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
	//���������Ӹ��� ���� 4:3�������������
	int				m_GridHorizonWid;	

	//ͼ��У׼�Ĵ��ڿͻ�������
	CPoint			m_AjustPoint[4];
	CPoint          m_AjustPointVL[4]; 

	BYTE*			m_pSelectAreaMark;		
	//BYTE*			m_pSelectAreaMarkBak;//���ο�����
	///��Ч������ͼ�񻺳�����ӳ��� 0X00 ������Ч��0X01 ������Ч��0X10 ��������
	BYTE*			m_pSelectAreaToImageBuffer; 

	int  m_stBlockX;		//����϶�����ʼ��x
	int  m_stBlockY;		//����϶�����ʼ��y
	//	int  m_prevBlockX;		//���ǰ���϶����Ŀ�x
	//	int  m_prevBlockY;		//���ǰ���϶����Ŀ�y
	int  m_curBlockX;		//��걾���϶����Ŀ�x
	int  m_curBlockY;		//��걾���϶����Ŀ�y
	bool m_bDrag;			//���ڽ��������ѡ

	//�����������ֿ����
	bool  SetGridHorizonNum(int wid ,int m_ImageWidth,  int  m_ImageHeight );
	//������Ч������������� ��ȷ������������Щ������Ч����Ч
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


	//5.ͼ��У׼ - ��ɼ������
	double			dbTranformMatrix[3][3];
	//�Ӻ���ͼ������õ��ɼ�������
	void GetVisualCoordinate(double TranformMatrix[3][3],double srcX,double srcY,double& reX,double& reY);//XY.1
	//���ת������
	bool GetTransformMatrix(POINT IrC[3],POINT VC[3],double TranformMatrix[3][3]);//XY.3
	//3*3��������
	bool Matrix3X3_Inverse(double Matrix[3][3],double Matrix_Inv[3][3]);	//XY.4
	//���ݶ��������Ƶ������ӳ���ϵ,Ҫ����ת������
	bool GetVideoTransform(bool bForce=true);	//XY.2  bForce==true ǿ����ת������
	bool			m_bHaveMap;			//�Ѿ���ӳ�����


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
