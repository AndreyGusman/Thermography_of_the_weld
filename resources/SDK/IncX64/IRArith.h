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




const short STACK_MAX_POINTS	=	30;  // 连通堆栈 大小   100
const short cMaxAlarmAreaCnt	=	5;		//最大为3	最大报警区域个数

class AFX_CLASS_EXPORT RegionGrowArith
{
public:
	RegionGrowArith(int wid ,int hei );
	~RegionGrowArith();
	
	//报警区域的个数
	int GetHighTempAreaNum();	
	void ImportMaskImg(unsigned char *input);
	unsigned char *GetRegionGrowImg(); 

	 LinkedAreaInfo* GetHighTempArea(); 
	//  // 1 increase  0 down    对结果排序， 只获取最后5 个， 并排序； 
	void  DealMultiAlarmData( short *img, int minad, int maxad ,int increase =1,int size_thr = 80, int dis_thr= 30 ) ;  
	void  DoEveryFrame();
	
private:
	void InitRegionGrowArith(); 
	void FreeRegionGrowArith();	

	int m_ImageWidth; 
	int m_ImageHeight; 

	int*			pnGrowQueX ;	//定义堆栈，存储坐标
	int*			pnGrowQueY ;	//定义堆栈，存储坐标
	int				iRegionMinNum;	//构成一个高温连通区域的点的最小数目
	
	//2.区域连通的相关计算
	BYTE*			pHighTempMark;	//高温点的标识	 采用 IRM 中的CHAR 图 中ISO  0.1.2 编号等， 这样复制过来。
	// 需要 每帧图像都要处理一遍。 注意。 
	
	LinkedAreaInfo  m_HighTempArea[STACK_MAX_POINTS];	//高温连通区域
	//先前帧信息	
	//	int				m_HighTempAreaNumPre;				//先前帧的高温连通区域的数目
	//	LinkedAreaInfo  m_HighTempAreaSum[STACK_MAX_POINTS];//前n帧的高温连通区域
	
	short			m_AlarmHighAD;	//报警的最高AD
	short			m_AlarmLowAD;	//报警的最低AD

	//高温连通区域的数目
	int				m_HighTempAreaNum;	//报警区域的个数

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
		int Mh_minPixelCnt =80,  //// 连通最小个数   Mh_minPixelCnt = 150 ？？
		int Mh_UBNeigh_MERGE_YDIFF =25	// Mh_UBNeigh_MERGE_YDIFF =25 	6;	  在X轴相差不大时(<25),上下
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
		int radius, // 半径 ， 最大 只有9*9 
		double SC, 
		double SS  ) ; 

	void AFX_CLASS_EXPORT JBF_8U_ARITH( unsigned char * src,  unsigned char * dst, 
							 short imgw, short imgh,  int radius // 半径 ， 最大 只有9*9 
							); 



#ifdef __cplusplus  
};  
#endif 



#endif 
