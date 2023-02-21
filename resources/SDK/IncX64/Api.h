#pragma once

#ifdef DLLPORT_EX  // define in c++ compile .
#define DLLPORT      __declspec(dllexport)
#else
#define DLLPORT      __declspec(dllimport)
#endif



// API 接口， 2010-10 V 1.3  
#define	CARD_MAX_NUMBER			16
#define	MAX_STRING_LEN			256

//最大等温带个数 
#define  MAX_ISO_THERM_NUM    5 


#define   IS_SIGNED_OR_UNSIGNED_DATA   //short 

#ifdef  IS_SIGNED_OR_UNSIGNED_DATA  
	#define   RAW_DATA_HAS_SIGN
	typedef   short  RAW_TYPE;
#else 
	typedef  unsigned short  RAW_TYPE;
#endif 

typedef short ADVALUETYPE;
typedef unsigned int UINT32;
typedef int INT32;
typedef float FLOAT32;
typedef double FLOAT64;
typedef unsigned long DWORD;

typedef short INT16;
typedef signed char  INT8; 


// 底层是不是使用千兆网  还是百兆网络 
// #define  GBIT_TTL   1    //
// typedef unsigned char UINT8;
// typedef char INT8;
// typedef unsigned short UINT16;
// typedef short INT16;

//added by jw 2017-03-02
typedef struct {
    char name[16];              ///< String containing the device's model name
    char transport[16];         ///< Serial | CoaXPress | GigEVision | Network | CameraLink
    char url[32];              ///< URL identifying the camera internally. e.g. cam://0..n
    char address[16];           ///< The address where the device resides, the format is protocl specific. e.g. 192.168.2.2 | COM0..n | CL0..n::NationalInstruments
    char interfaceName[16];
    char serial_num[16];        ///< Serial number reported by the camera. e.g. "12345678"
    unsigned int pid;           ///< Product id reported by the camera. e.g. 0x0000F020
    unsigned short width;
    unsigned short height;
} DeviceInformation;

typedef enum
{
    EF_NULL            = 0x00000000,
    EF_Network         = 0x00000001,   ///< Network
    EF_Serial          = 0x00000002,   ///< Serial
    EF_CameraLink      = 0x00000004,   ///< CameraLink
    EF_GigEVision      = 0x00000008,   ///< GigEVision
    EF_CoaXPress       = 0x00000010,   ///< CoaXPress
    EF_USB             = 0x00000020,   ///< USB
    EF_USB3            = 0x00000040,   ///< USB3.0
    EF_EnableAll       = 0x0000FFFF,   ///< Enable all protocols.
    EF_UseCached       = 0x01000000,   ///< Use cached devices on enumeration.
    EF_ReleaseCache    = 0x02000000,   ///< Release internally cached devices. 
} EnumerationFlag;

typedef struct tagStorProp
{
    unsigned char type;//image or video
    unsigned char status;//unknown,unused,used
    unsigned short index;//image or video index
    unsigned short frameCnt;//image count written in a video
    unsigned short resv;
} StorProp;


//added by jw 2018-01-02
typedef struct tagCameraConfig
{
	//add by yzw 2018
	char detector_type[16];
	char detector_serial_num[16]; //  for net mac ip 
	char device_model[16];
	char device_comm_if_type0[16];
	char device_comm_if_type1[16];

	unsigned int integrationTimeMin;
	unsigned int integrationTimeMax;
	unsigned int integrationTime;

	unsigned short VSK;
	unsigned short GFID;
	unsigned short VBUS;
	unsigned short GSK;

	short autoExposureMode;

	short tecMode;
	short tecObject;
	unsigned short pidP;
	unsigned short pidI;
	unsigned short pidD;

	unsigned short frameFrequencyDivider;

	unsigned short sensorGain;
	unsigned short sensorGainCount;
	unsigned short sensorGainArray[4];
	unsigned short sensorOutputMode;
	unsigned short sensorOutputModeCount;
	unsigned short sensorOutputModeArray[4];
	unsigned short sensorReadOrder;
	unsigned short sensorChannelRevert;//swap channel output order
	unsigned short sensorTestPattern;
	unsigned short sensorBias;
	unsigned short sensorCDSMode;//0~non CDS,1~CDS
	unsigned short sensorReference;//0~signal,1~reference

	int  sensorPhaseObject; //add  2018.6 
	unsigned char sensorTrigMode; // 将来添加 
	short   col_arith_type; //add 2018.12 
	short   col_add[4];
	short   col_add2[4] ; //  

	//add 2020.6 for test p 
	//
	unsigned short  mainfreq; 
	unsigned short  adcn ; 
	//  frameFrequencyDivider     !!!
	float  sysK;
	float  sysB;
	short  limtup;
	short  limtdown;
	  


	
} CameraConfig;


// 外部测温模式下，用户参考区域导入结构体
typedef struct  _USER_REFAREA_
{
	short   bUseRefArea;        //是否使用参考区测温，0 否  1 是
	short   RefAreaUpX;         //参考区域 左上 角 和右 下角 坐标
	short   RefAreaUpY; 
	short   RefAreaDownX; 
	short   RefAreaDownY; 
	short   RefAreaTemp;        //参考区域均值 温度 *  10 
	short   RefAreaAD;          //参考区域 均值 内部返回 
}USER_REFAREA;



enum STREAM_TYPE
{
	IRDATA_NONE =0 ,
	IRDATA_ONLINESTREAM =1,
    IRDATA_VIDEO =2,
    IRDATA_RAWFILE =3 
};

enum IR_DEVICE_TYPE
{
	UNDEFINE =0,
	IRGBIT =1,
	IRMBIT =2,
	IRUSBFT=3,
	IRGIGE =4,
	IIVFILE =5,
	TVIDEOFILE =6,
	TRAWFILE =7,  //BMP 
	TRAWRAWFILE =8, //raw 
	IR_CL_ADLINK =9 ,  // CAMLINK
	IR_SIM_DEV =10,
	NODEVICE =20
};

// ADD 2016.8  添加了直方图的信息； 

#define  HISTOGRAM_BIN_CNT    512 
typedef struct  _HISTOGRAM_INFO_
{
	int  LEN; 

	RAW_TYPE  MAX;
	RAW_TYPE  MIN; 
	RAW_TYPE  CUT_MIN; 
	RAW_TYPE  CUT_MAX; 
	int TOP_CUT ; // 千分比
	int BOT_CUT ; // 千分比
		
	unsigned int BIN[HISTOGRAM_BIN_CNT];  // 一般就考虑256 因为用户一般也 用不到更高的 
	char bUseAllData;   //  1 使用全部区域数据， 0 使用CUT 后的
}IR_16BIT_HISTOGRAM_INFO, *PIR_16BIT_HISTOGRAM_INFO;

#define  HISTOGRAM_LIMIT_CUT_CNT   128  


typedef struct  _CALLBACK_STREAMINFO_
{
	unsigned int  Heigth;      // image hei
	unsigned int  Width;       // image wid
	unsigned int  Length;      // image size , byte S，
}IR_CALLBACKIMAGEINFO, *PIR_CALLBACKIMAGEINFO;

// curr .only support gbit device ... other device will update to surport this func..
typedef BOOL (WINAPI *CALLBACKFUNC)( void* pData, PIR_CALLBACKIMAGEINFO pImageInfo, void* pUserData );

typedef void * GHDEV_HND; // 64 BIT USE THIS TO CHANGE  int handle.

#include "userdef.h"  // OLD VERSION PORT ... 

extern "C" { 
	
    void DLLPORT IR_Init();   //系统初始化 
	
	//SDK version:[15:12]~major version, [11:8]~minor version, [7:0]~revision
	int DLLPORT IR_GetVersion(unsigned short *version);

	int DLLPORT IR_GetRevisionTime(char *buff, unsigned int buff_len);
	
    int  DLLPORT IR_GetFrames();

	//added by jw 2018-01-02 消耗时间较长 
	BOOL DLLPORT IR_GetCameraConfig(GHDEV_HND handle, CameraConfig *config);

    //change from 2017 
    int DLLPORT IR_EnumerateDevices(DeviceInformation *deviceInfomation, unsigned int *deviceCount, EnumerationFlag flags);

    int DLLPORT IR_FreeDevices(void);

    GHDEV_HND DLLPORT IR_OpenDevice(GHDEV_HND  hwnd, char *name);

    int DLLPORT IR_AddMessageFilter(GHDEV_HND handle, MessageFilter filter, void *pUserData);

	float DLLPORT  IR_GETDeviceFPS(GHDEV_HND handle);  // ADD 2018 

    BOOL DLLPORT IR_IsOpen(GHDEV_HND handle); 
    BOOL DLLPORT IR_Close(GHDEV_HND handle);          
    BOOL DLLPORT IR_Reset(GHDEV_HND handle);

	enum STREAM_TYPE DLLPORT  IR_GetHandleType(GHDEV_HND handle); 
	enum IR_DEVICE_TYPE  DLLPORT  IR_GetHandleTypeExt(GHDEV_HND handle); 


	// 打开RAW 数据 IRP 
	GHDEV_HND  DLLPORT IR_RawImageOpen(char * pszFileName); 
	// 打开视频文件 IRM 
	GHDEV_HND  DLLPORT IR_MovieFileOpen( char*  FileName);  

	// 硬件控制 
	BOOL DLLPORT IR_SendSeriaPortCmd(GHDEV_HND handle, unsigned char *buff ,int len);      
	BOOL DLLPORT IR_ReceiveSeriaPortCmd(GHDEV_HND handle,unsigned char *buff ,int *len, unsigned short *id); 
	BOOL DLLPORT IR_Calibrate(GHDEV_HND handle);
	BOOL DLLPORT IR_SoftCalibrate(GHDEV_HND handle); 
	// SUB IS OLD HARDWARE SUPPORT .
    BOOL DLLPORT IR_NearFocus(GHDEV_HND handle);      
    BOOL DLLPORT IR_FarFocus(GHDEV_HND handle);	
	BOOL DLLPORT IR_StopFocus(GHDEV_HND handle);	
	
	BOOL DLLPORT IR_CalibrateP1(GHDEV_HND handle);      //两点校正 点1 
	BOOL DLLPORT IR_CalibrateP2(GHDEV_HND handle);      //两点校正 点2
	BOOL DLLPORT IR_CalibrateReset(GHDEV_HND handle);   //两点校正清空
	// 2019.2 ADD  FOR MULTI CHAN  , IF not set ,will use the default chan 0.
	//  USER CAN CHANGE SET CHAN FROM 0 (DEFAULT CHAN) TO  MAX  MAX_MULTI_DANG_NUM (8) 
	BOOL DLLPORT IR_CalibrateSetCurrChan(GHDEV_HND handle, int index) ; //(0--8)
	int  DLLPORT IR_CalibrateGetCurrChan(GHDEV_HND handle); // -1 is error ..
	BOOL DLLPORT IR_ReadDataCalcK(GHDEV_HND handle, LPCTSTR file1,LPCTSTR file2);

	// 红外图像与数据 处理 
    BOOL DLLPORT IR_TransmitArray(GHDEV_HND handle, unsigned char *pData, int len, int type);
	BOOL DLLPORT IR_GetNewArray(GHDEV_HND handle); //得到新的一副图像
	BOOL DLLPORT IR_GetNewArrayDirect(GHDEV_HND handle); //得到新的一副图像 ADD 2018.10 为了高速图像获取省去了软件层面的再处理

	BOOL DLLPORT IR_SetCallBackFun( GHDEV_HND handle, CALLBACKFUNC pCallBack, void* pUserData ); // 采用回调函数方式获取图像信息，
    BOOL DLLPORT IR_TransmitDataTypeSet(GHDEV_HND handle, short  datatype );  //type 1  y16  2  x16  type 3  netrecdata
	BOOL DLLPORT IR_TransmitBadPointFile(GHDEV_HND handle);

    BOOL DLLPORT IR_SwitchVideoMode(GHDEV_HND handle, short mode);//0-Normal(数字和模拟视频共享带宽),1-Digital(数字视频独占带宽)

    //温度AD矩阵
    double DLLPORT IR_GetDigitVal(GHDEV_HND handle, short x, short y);
    BOOL  DLLPORT IR_GetDigitArray(GHDEV_HND handle, void * const pRawShortData);
    BOOL  DLLPORT IR_GetDigitArrayPara(GHDEV_HND handle, int *iWidth,int *iHeight); 
	void  DLLPORT IR_GetCurrMinAndMaxDigitVal(GHDEV_HND handle,int *wMax,int *wMin); 

	// 2016.9 升级了直方图映射的 底层； 
	// BOOL DLLPORT IR_DigitArrayToBmp(GHDEV_HND handle, const short * const pRawShortData,BYTE * const pBmpData);
	BOOL DLLPORT IR_DigitArrayToBmp(GHDEV_HND handle, const short * const pRawShortData,BYTE * const pBmpData,int isRGB,  IR_16BIT_HISTOGRAM_INFO *pHistGram);
    
	// 亮度对比度调节的控制 
	// 2018.5 为台湾客户 增加全手动亮度对比度算法。 
	// 之前亮度对比度，为观瞄客户需要的调节方法。 
//	BOOL  DLLPORT IR_SetAutoBrihgtContrast(int handle, BOOL bAuto);   
//	int   DLLPORT IR_GetAutoBrihgtContrast(int handle);
	//替换上两个函数， 转化为类型设置 
	// 0 自动两对对比度 ， 1  观瞄 手动亮度对比度， 2  全手动亮度对比度 
	BOOL  DLLPORT IR_SetBrihgtContrastType(GHDEV_HND handle, int type);  
	int   DLLPORT IR_GetBrihgtContrastType(GHDEV_HND handle);

	int   DLLPORT IR_GetCurrContrast(GHDEV_HND handle);   
	int   DLLPORT IR_GetCurrBright(GHDEV_HND handle);     

	BOOL  DLLPORT IR_SetCurrContrast(GHDEV_HND handle, int contrast);   
	BOOL  DLLPORT IR_SetCurrBright(GHDEV_HND handle,int bright);     

    // SUB INFO GET FROM IMAGE PARALINE ... 
    short DLLPORT IR_GetVTempFPA(GHDEV_HND handle);
    unsigned int DLLPORT IR_GetFrameID(GHDEV_HND handle);
	//ADD 2019 FOR ULIS 
	unsigned int   DLLPORT IR_GetCurrIntTime(GHDEV_HND handle);
	unsigned char  DLLPORT IR_GetCurrGain(GHDEV_HND handle);	
	short  DLLPORT IR_GetCurrBAve(GHDEV_HND handle);	
	short  DLLPORT IR_GetCurrBvt(GHDEV_HND handle);

	unsigned short DLLPORT IR_GetULIS_GFID(GHDEV_HND handle);  // FOR DEBUG 
	unsigned short DLLPORT IR_GetULIS_GSK(GHDEV_HND handle) ; 
	unsigned short DLLPORT IR_GetCurrFrameDiv(GHDEV_HND handle); 

	
	// 伪彩色调色板
	int DLLPORT IR_GetCurrPalette(GHDEV_HND handle, RGBQUAD *pPal);
	// 设置调色板为厂家 定义的index号标准调色板，并返回调色板内容  调色板结构为256个RGBQUAD
    BOOL DLLPORT IR_SetPalette(GHDEV_HND handle, int index,RGBQUAD *pPal);			//
	// 设置调色板为厂家 定义的index号标准调色板，并返回调色板内容  调色板结构LONG[256]，R<<16 + G<<8 + B 组合成LONG 结构
	BOOL DLLPORT IR_SetPaletteLong(GHDEV_HND handle,int index,unsigned int  * pPal);	//返回调色板信息
	// 将当前使用的调色板设置为 用户自己定义的 输入pPal 为RGBQUAD[256] 
	BOOL DLLPORT IR_SetUserPalette(GHDEV_HND handle,RGBQUAD *pPal); 

	//数据保存 
	BOOL DLLPORT IR_SaveCurrImage(GHDEV_HND handle,char *lpszPathName);  // ghopto bmp.  and raw file 
	BOOL DLLPORT IR_SaveCurrImageAsBmp(GHDEV_HND handle, char *lpszPathName);

	BOOL   DLLPORT IR_IsRecordingMovie(GHDEV_HND handle) ; 
	DWORD  DLLPORT IR_StartRecordMovie(GHDEV_HND handle, char* szScopeFile); 
	DWORD  DLLPORT IR_StopRecordMovie(GHDEV_HND handle); 

	//历史数字视频录像的 播放 

	BOOL DLLPORT IR_MoviePause(GHDEV_HND handle,BOOL bPause);//暂停播放录像  
	BOOL DLLPORT IR_MovieIsPause(GHDEV_HND handle);                         
	BOOL DLLPORT IR_MovieForward(GHDEV_HND handle,unsigned int nFrame);       
	BOOL DLLPORT IR_MovieBackward(GHDEV_HND handle,unsigned int nFrame);      
	BOOL DLLPORT IR_SetCyclePlay(GHDEV_HND handle,BOOL set );//录像是否循环播放 
	BOOL DLLPORT IR_IsCyclePlay(GHDEV_HND handle);//录像是否循环播放 
	                                             
	BOOL DLLPORT IR_MovieGoto(GHDEV_HND handle,int setindex);// 设置当前播放文件位置帧序号  
	int  DLLPORT IR_MovieGetPosi(GHDEV_HND handle); //得到当前播放文件 位置 
	int  DLLPORT IR_MovieGetTotalFrm(GHDEV_HND handle); //得到播放文件总长度 
	

	short DLLPORT IR_GetAmbientTemp(GHDEV_HND handle);
	short DLLPORT IR_GetAtmosphereTempH(GHDEV_HND handle);

    short DLLPORT IR_GetVTemp(GHDEV_HND handle);
	BOOL DLLPORT IR_GetDeviceIRIParam(GHDEV_HND handle, void **returnpt ) ; 
	//  注意 这个 函数操作的高风险区域指针 ， 不要乱改。 
//---------------------------------------------

	// SUB ONLY SUPPORT CAMLINK PORT CAMERA ..
	BOOL  DLLPORT IR_CaptureReset(GHDEV_HND devHandle);
	BOOL  DLLPORT IR_SetExtTrigger(GHDEV_HND devHandle, int total_cycle_us,int pulse_wid_us);
	BOOL  DLLPORT IR_GetExtTrigger(GHDEV_HND devHandle, int *total_cycle_us,int *pulse_wid_us);

	BOOL  DLLPORT IR_GetDeviceConPath(GHDEV_HND handle, char *path) ; // input must len>=256 

//----------------------------------------- for debug -------------------
	unsigned int DLLPORT IR_GetDeviceID(GHDEV_HND handle); 
	BOOL DLLPORT IR_SaveCurrImageV1D7(GHDEV_HND handle,char *lpszPathName, BITMAPINFOHEADER infohead , BYTE * m_bmiColors, BYTE *pBits); //ADD 2020

	BOOL DLLPORT IR_SHANGHAI_ARITH(GHDEV_HND handle,short* output);//暂停播放录像  

	float DLLPORT IR_GH640V1_TtoAD(float tempval); 
	float DLLPORT IR_GH640V1_ADtoT(float ad); 




};