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
	

//�㷨��ʹ�õģ� ע����ⲿͬ��



//#define   USE_TEXTURE_ARITH   1   //�����㷨
//#define   USE_OLD_YANWU_ARITH   1   USE_SHUWEN_ARITH  //�ϵ� �������㷨2011�㷨
//#define   USE_ENHANCE_ARITH   1   //ͼ����ǿ


//2010.3.16 ���� ȥ ���ƴ���TTL

// #define  MANUAL_DEL_TEXTURE      1    //�ֶ�ȥ����  ����   ������� ����ȥ���� �� ���ǣ� 

// ��Ҫ�Ľӿ� �� �ɰ���  �ɹ��� �� �ɼ�������
// ��ÿ��ͼ�����㷨���� ��



#define  NO_USE_SECONDE_BP_DEAL    1

//�Ƿ���չ�������ͣ�������8�����ͣ��������4������  Ŀǰ��ʱ��ʹ�� ��  
//#define EXTEND_BAD_POINT_TYPE 


#include "api.h" //add 2018  for raw data has sign or not 




typedef  struct  tagBADPOINT
{
	int X ;
	int Y ;
	int Direction;
}BADPOINT;


typedef struct tagRegionObj{ 
	POINT	pt;		//����ԭʼ����λ��
	//float	temperature;//�¶�
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
	short   MaxGray;    // ���AD 2020 ADD .
	short   MinGray;    //
	short	MeanGray;	// ƽ��ADֵ
	POINT	ptMaxTempImg;	//����¶ȵ�ͼ������	
	POINT   ptMinTempImg;   //��� 
	POINT	ptCentroidImg;  //���ĵ�ͼ������
	
	int		iCount;  //����
	int     minX;    //ADD 2020 
	int     maxX; 
	int		minY;    // ���������С ��������
	int		maxY;
	int     iAreaPiexNum; //�����ĸ���  //ADD BY YZW  12-15
	
	// �û���������
	//POINT	ptMaxTempScreen;	//����¶ȵĴ�������
	//POINT	ptCentroidScreen; //���ĵ���Ļ����
	//float   MaxTemp;	//����¶�	
	//float   MeanTemp;	//ƽ���¶�
	
}LinkedAreaInfo;//������ͨ����


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
		return 	imgMark; //����ͼ
	}

	void  SetBpImage(short *image)
	{
		memcpy(imgMark,image,m_ImageSize *sizeof(short) ) ; //   ���浽 �ļ����� 
	}

	void	ReadDataCalcK(LPCTSTR szPath);  // READ N1 ,N2  RAW CALCK .
	void    ResetTwoPT(); 
	void    ReadRawDataCalcK(LPCTSTR file1, LPCTSTR file2);
	void	ReadRawDataCalcK(LPCTSTR szPath);

	void	ResetK();
	
	float	GetStandAverage(int bIsB1B2orOriData=0,RAW_TYPE* pSrc=NULL);


	bool   m_bUserArith;  //�Ƿ�ʹ���㷨 

//	 short   m_ArithType;  //��ǰ�㷨�� ����  
//   short   m_xishu[10];

//----------���Ӷ� RAW �ļ���֧��  ---------//
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
	short *imgMark; //����ͼ

	float *imgLBuff;
	float *imgHBuff;
	int  mLBuffCnt;
	int  mHBuffCnt;

	TCHAR  m_Path[256];   // KDATA ����ĵط� 
	TCHAR  m_deviceStr[16]; //

	//add 2015.4 ���AFFINE �任��Ҫ�Ĳ��������ǵ�û�� PARA �����ˣ�ʹ��INI ��ʽ���ã�
	// �������� INI �� �豸���ֹ�������������ʵ�֡� ???????
	int  IniPara[128]; //

	IRArith *m_pParent;  

    //CImageCorrection m_imgCorr;  // Ŀǰû������ 

private:
	// 2019.2 Ϊ���� ��Ŀ��� 
	//m_xishu[1]  index ; 
	int  m_is_use_mutidang; //����    // 0,1,2,3,4,5,6,7, .... ����൵λ�� -1 ���� Ŀǰ��Ϣ�� 
	int  m_curr_dang_index; // ��ǰ��λ Ĭ��Ϊ 0 �� ����Ϊ�൵�� 1��2��3  MAX_MULTI_DANG_NUM

	int *imgL_MULTI[MAX_MULTI_DANG_NUM];   int  AVE_L_MULTI[MAX_MULTI_DANG_NUM] ; 
	int *imgH_MULTI[MAX_MULTI_DANG_NUM];  // ���� K 	
	

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