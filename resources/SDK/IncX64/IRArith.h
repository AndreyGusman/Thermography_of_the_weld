#ifndef  __CALCK___
#define  __CALCK___

#include "def.h"

#define SG_FREE_SAFE(PTR)			{ if( PTR ) { SG_Free (PTR); PTR = NULL; } }
#define SG_DELETE_ARRAY(PTR)		{ if( PTR ) { delete[](PTR); PTR = NULL; } }


class AFX_CLASS_EXPORT IRArith
{
public:
	IRArith();
	~IRArith();
	
	void	Init(int nImageX,int nImageY,LPCTSTR  szPath ,LPCTSTR strKbKey=_T(""));
	
    //added by jw 2016-11-05
    void    SaveBP(short *pData);

	void	CalcK(); // const char* tKBno=""
	void    SetLData(short *input,int n);
	void    SetHData(short *input,int n);
	void    ResetTwoPT();
	int     SetCurrChan(int index); 
	int     GetCurrChan(); 
	bool    GetLData(int cSysL_Marge=0,bool bUpdateL=true);
	void    GetHData();
	void    GenY16(short *pOut,BOOL bUseArith=false, BOOL bCorre=FALSE,int nThres=300);
	void    ReadRawDataCalcK(LPCTSTR file1, LPCTSTR file2);
	
	void	GetArithPara(short xishu[10]);
	bool    SetArithPara(short xishu[10]);

	void   SetArithType(int type);
	int    GetCurrArithType( );

	// 8 BIT ARITH  
	void   PHE_8BIT( unsigned char *  pInput, unsigned char *pOut, int nWidth, int nHeight);
	void   PHE_16BIT(const short * const pInput, unsigned char *pOut,int th1, int th2,  int nWidth, int nHeight);
	void   AR_PHE2_HIGHPASS(const short *dataCurr0,unsigned char *pOut, int width,int height, int xishu )  ;


	short   m_para[10];

	short*  GetArithBpImage( );
	void    SetArithBpImage( short *image );

	IRCalcK *myLib;
};




const short STACK_MAX_POINTS	=	30;  // ��ͨ��ջ ��С   100
const short cMaxAlarmAreaCnt	=	5;		//���Ϊ3	��󱨾��������

class AFX_CLASS_EXPORT RegionGrowArith
{
public:
	RegionGrowArith(int wid ,int hei );
	~RegionGrowArith();
	
	//��������ĸ���
	int GetHighTempAreaNum();	
	void ImportMaskImg(unsigned char *input);
	unsigned char *GetRegionGrowImg(); 

	 LinkedAreaInfo* GetHighTempArea(); 
	//  // 1 increase  0 down    �Խ������ ֻ��ȡ���5 ���� ������ 
	void  DealMultiAlarmData( short *img, int minad, int maxad ,int increase =1,int size_thr = 80, int dis_thr= 30 ) ;  
	void  DoEveryFrame();
	
private:
	void InitRegionGrowArith(); 
	void FreeRegionGrowArith();	

	int m_ImageWidth; 
	int m_ImageHeight; 

	int*			pnGrowQueX ;	//�����ջ���洢����
	int*			pnGrowQueY ;	//�����ջ���洢����
	int				iRegionMinNum;	//����һ��������ͨ����ĵ����С��Ŀ
	
	//2.������ͨ����ؼ���
	BYTE*			pHighTempMark;	//���µ�ı�ʶ	 ���� IRM �е�CHAR ͼ ��ISO  0.1.2 ��ŵȣ� �������ƹ�����
	// ��Ҫ ÿ֡ͼ��Ҫ����һ�顣 ע�⡣ 
	
	LinkedAreaInfo  m_HighTempArea[STACK_MAX_POINTS];	//������ͨ����
	//��ǰ֡��Ϣ	
	//	int				m_HighTempAreaNumPre;				//��ǰ֡�ĸ�����ͨ�������Ŀ
	//	LinkedAreaInfo  m_HighTempAreaSum[STACK_MAX_POINTS];//ǰn֡�ĸ�����ͨ����
	
	short			m_AlarmHighAD;	//���������AD
	short			m_AlarmLowAD;	//���������AD

	//������ͨ�������Ŀ
	int				m_HighTempAreaNum;	//��������ĸ���

	void RegionGrow(ADVALUETYPE* pImage,int m_ImageWidth, int m_ImageHeight, 
		CPoint &ptSeed,CPoint &ptCentroid,
		RegionOBJ &IrMaxTempInArea,RegionOBJ &IrMinTempInArea,
		int &iAreaObjectNum,int &iAreaSumAd,int* pMlthgNum, 
		CPoint* ptNormalCentr,
		int* minAreaY,int* maxAreaY, int* minAreaX,int* maxAreaX, 
		int AlarmLowAD, int AlarmHighAD ) ; 

	void GetFrameAlarmAreaMlthg(ADVALUETYPE* pAdArray,
		int m_ImageWidth,int m_ImageHeight,
		int AlarmLowAD, int AlarmHighAD , 
		int Mh_minPixelCnt =80,  //// ��ͨ��С����   Mh_minPixelCnt = 150 ����
		int Mh_UBNeigh_MERGE_YDIFF =25	// Mh_UBNeigh_MERGE_YDIFF =25 	6;	  ��X������ʱ(<25),����
							); 

};

//ADD 2019 FOR C FUNC 


#ifdef __cplusplus  
extern "C" {  
#endif 

	char AFX_CLASS_EXPORT * UnicodeToAnsi(const wchar_t* szStr)  ;
	wchar_t AFX_CLASS_EXPORT * AnsiToUnicode(const char* szStr); 
	char AFX_CLASS_EXPORT * UnicodeStringToAnsic(CString str1); 

	double AFX_CLASS_EXPORT CStringToDouble( CString str); 

	// mem 
	void  AFX_CLASS_EXPORT  *	SG_Malloc			(size_t size);
	void  AFX_CLASS_EXPORT  *	SG_Realloc			(void *memblock, size_t size);
	void  AFX_CLASS_EXPORT		SG_Free				(void *memblock);


	void AFX_CLASS_EXPORT JBF_8U_INIT(  
		short imgw, short imgh, 
		int radius, // �뾶 �� ��� ֻ��9*9 
		double SC, 
		double SS  ) ; 

	void AFX_CLASS_EXPORT JBF_8U_ARITH( unsigned char * src,  unsigned char * dst, 
							 short imgw, short imgh,  int radius // �뾶 �� ��� ֻ��9*9 
							); 



#ifdef __cplusplus  
};  
#endif 



#endif 
