#ifndef  __DEF_H__
#define  __DEF_H__

#ifdef DLLPORT_EX
#define DLLPORT      __declspec(dllexport)
#else
#define DLLPORT      __declspec(dllimport)
#endif


#define  MAX_IMAGE_BUFFER_SIZE   (1280*1024*2)


#define  DEFAULT_IMAGE_WID     640
#define  DEFAULT_IMAGE_HEI     512
	

//算法中使用的， 注意和外部同步



//#define   USE_TEXTURE_ARITH   1   //暗纹算法
//#define   USE_OLD_YANWU_ARITH   1   USE_SHUWEN_ARITH  //老的 气体检测算法2011算法
//#define   USE_ENHANCE_ARITH   1   //图像增强


//2010.3.16 增加 去 暗纹处理TTL

// #define  MANUAL_DEL_TEXTURE      1    //手动去暗纹  锅盖   否则计算 方法去暗纹 和 锅盖， 

// 需要的接口 ， 采暗纹  采锅盖 ， 采集方法，
// 对每个图像做算法工作 ，



#define  NO_USE_SECONDE_BP_DEAL    1

//是否扩展坏点类型，即采用8种类型，否则采用4种类型  目前暂时不使用 ；  
//#define EXTEND_BAD_POINT_TYPE 


#include "api.h" //add 2018  for raw data has sign or not 




typedef  struct  tagBADPOINT
{
	int X ;
	int Y ;
	int Direction;
}BADPOINT;


typedef struct tagRegionObj{ 
	POINT	pt;		//红外原始坐标位置
	//float	temperature;//温度
	ADVALUETYPE	 adValue;
	tagRegionObj()
	{
		ZeroMemory(this,sizeof(tagRegionObj));
	}
	tagRegionObj(const tagRegionObj& rhs)
	{
		pt	=	rhs.pt;		
		//	temperature=rhs.temperature;	
		adValue	=	rhs.adValue;
	}
	tagRegionObj& operator=(const tagRegionObj& rhs)
	{
		pt	=	rhs.pt;	
		//	temperature=rhs.temperature;	
		adValue	=	rhs.adValue;
		return	(*this);
	}
}RegionOBJ;

typedef struct tagLinkedAreaInfo{ 
	short   MaxGray;    // 最高AD 2020 ADD .
	short   MinGray;    //
	short	MeanGray;	// 平均AD值
	POINT	ptMaxTempImg;	//最高温度的图像坐标	
	POINT   ptMinTempImg;   //最低 
	POINT	ptCentroidImg;  //质心的图像坐标
	
	int		iCount;  //计数
	int     minX;    //ADD 2020 
	int     maxX; 
	int		minY;    // 坐标最大，最小 用于区域
	int		maxY;
	int     iAreaPiexNum; //区域点的个数  //ADD BY YZW  12-15
	
	// 用户附带数据
	//POINT	ptMaxTempScreen;	//最高温度的窗口坐标
	//POINT	ptCentroidScreen; //质心的屏幕坐标
	//float   MaxTemp;	//最高温度	
	//float   MeanTemp;	//平均温度
	
}LinkedAreaInfo;//高温连通区域


#define  MAX_MULTI_DANG_NUM     8  // 2019 FOR CHANGCHUN ...


class AFX_CLASS_EXPORT IRArith; 

class IRCalcK
{
	
public:
	IRCalcK();
	~IRCalcK();
    void    InitArithParam(short arithType);
	void	Init(int nImageX,int nImageY,LPCTSTR szPath,IRArith *pParent=NULL,LPCTSTR strKbKey=_T(""));
	void	FreeTwoPointAjustRes();

    //added by jw 2016-11-05
    void    SaveBP(short *pData);

	void	CalcK();  //const char* tKBno=""
	void    SetLData(short *input,int n);
	void    SetHData(short *input,int n);
	bool    GetLData(int cSysL_Marge=0,bool bUpdateL=true);
	void    GetHData();
	void    GenY16(short *pOut,BOOL bUseArith=FALSE, BOOL bDynRmvShandian=FALSE,int nShandianThres=300);

	int   SET_MULTI_CURR_DANG(int index);
	int   GET_CURR_DANG(); 

	short*    GetBpImage()
	{
		return 	imgMark; //坏点图
	}

	void  SetBpImage(short *image)
	{
		memcpy(imgMark,image,m_ImageSize *sizeof(short) ) ; //   保存到 文件中区 
	}

	void	ReadDataCalcK(LPCTSTR szPath);  // READ N1 ,N2  RAW CALCK .
	void    ResetTwoPT(); 
	void    ReadRawDataCalcK(LPCTSTR file1, LPCTSTR file2);
	void	ReadRawDataCalcK(LPCTSTR szPath);

	void	ResetK();
	
	float	GetStandAverage(int bIsB1B2orOriData=0,RAW_TYPE* pSrc=NULL);


	bool   m_bUserArith;  //是否使用算法 

//	 short   m_ArithType;  //当前算法的 类型  
//   short   m_xishu[10];

//----------增加对 RAW 文件的支持  ---------//
	void	ReadRawDataCalcK_path(LPCTSTR szPath);
	void	ReadRawDataCalcK_file(LPCTSTR file1, LPCTSTR file2);
private:
	bool   LoadRawLHKData(LPCTSTR szFile,int iDataLen ,int  * pB1B2Data);
	bool   SaveRawLHKData(LPCTSTR szFile,int iDataLen,int * pB1B2Data);
	bool   SaveRawBadPointReport(LPCTSTR szFile,int nNum,BADPOINT * pBadPoint);
    bool   LoadRawData(LPCTSTR szFile,int nNum,short * pData);
    bool   SaveRawData(LPCTSTR szFile,int nNum,short * pData);
    bool   SaveTextData(LPCTSTR szFile,int nNum,unsigned int * pData);
	void   CombinBdatBp(int *Ldata);
	void   CombinKB(int *Kdata);

private:

	long htoi(LPCTSTR str);
	bool LoadLHKData(LPCTSTR szFile,int iDataLen ,int  * pB1B2Data);
	bool SaveLHKData(LPCTSTR szFile,int iDataLen,int * pB1B2Data);
	bool SaveBadPointReport(LPCTSTR szFile,int nNum,BADPOINT * pBadPoint);

public:
    void CombinMBp();
    void CombinBBp();
	void Copy(IRCalcK* pSrc);
	void SaveNowStatus();
	void ReplaceBadPixel( short*pSrc,int nWidth, int nHeight,bool bDynRmvShandian=false,int nShandianThres=300);

private:
	int*	tmpData;
    __int64	    lMin[3], lMax[3],Sum[3]; // 32BIT  
	double lblAver[3];
	int    nBadDot ;
	BADPOINT BadDotsList[5000];

	int m_ImageX	;	
	int m_ImageY	;	
	int m_ImageSize	;
	
	bool  bHaveK; //ADD 2020 FOR QUICK DO 
	bool  bHaveB;
	bool  bHaveBP;

	int *imgL;       int AVE_L ;   //2020         
	int *imgH;
	int *imgK;
	short *imgMark; //坏点图

	float *imgLBuff;
	float *imgHBuff;
	int  mLBuffCnt;
	int  mHBuffCnt;

	TCHAR  m_Path[256];   // KDATA 保存的地方 
	TCHAR  m_deviceStr[16]; //

	//add 2015.4 添加AFFINE 变换需要的参数，考虑到没有 PARA 好用了，使用INI 方式配置，
	// 将来考虑 INI 和 设备名字关联起来，将来实现。 ???????
	int  IniPara[128]; //

	IRArith *m_pParent;  

    //CImageCorrection m_imgCorr;  // 目前没有启用 

private:
	// 2019.2 为长春 项目添加 
	//m_xishu[1]  index ; 
	int  m_is_use_mutidang; //？？    // 0,1,2,3,4,5,6,7, .... 代表多档位， -1 代表 目前信息； 
	int  m_curr_dang_index; // 当前档位 默认为 0 ， 否则为多档的 1，2，3  MAX_MULTI_DANG_NUM

	int *imgL_MULTI[MAX_MULTI_DANG_NUM];   int  AVE_L_MULTI[MAX_MULTI_DANG_NUM] ; 
	int *imgH_MULTI[MAX_MULTI_DANG_NUM];  // 代替 K 	
	

	void  MULTI_DANG_Init();
	void  MULTI_DANG_SetLoad(); // INIT FROM FILE 
	int   MULTI_DANG_SetLoadInd( int index ) ; 
	void  MULTI_DANG_ResetKL(int i); // INIT FROM FILE 

	
	void  MULTI_DANG_Free(); 
	void  MULTI_DANG_Save(int i );
	
};



extern "C" { 
	
//----------------------------------------- for debug -------------------
	// ADD 2020 FOR TEMP BMP FILE  DATA 
	int  DLLPORT  IR_GetAnalysisBlock(GHDEV_HND handle,char **retpt);   // FROM FILE TO  MEM 
	BOOL  DLLPORT  IR_ImportAnalysisBlock(GHDEV_HND handle,char *data, int datalen);   // FROM MEM TO FILE 
	BOOL  DLLPORT  IR_ImportAlarmMask(GHDEV_HND handle,unsigned char *data); 
//	short  DLLPORT IR_GetValidRegionNum(GHDEV_HND handle) ; 
//	BOOL  DLLPORT  IR_GetValidRegionInfo(GHDEV_HND handle , LinkedAreaInfo ** pout ); 

}

#endif 