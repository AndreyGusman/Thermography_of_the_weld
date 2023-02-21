

#ifndef  __USERDEF__H__  
#define  __USERDEF__H__  


#ifdef DLLPORT_EX  // define in c++ compile .
#define DLLPORT      __declspec(dllexport)
#else
#define DLLPORT      __declspec(dllimport)
#endif

typedef short INT16;
typedef signed char  INT8; 
//--------------------------------------------------------------------------------------------//
// CHANGE 2018.6  ,  COLLECT TEMP CAL TO THIS FILE ....

//max temperature iso 
#define   MAX_ISO_THERM_NUM    5 

#define   MAX_TEMP_OBJCTS_NUM   5



#define CURVE_LENGTH   16384   //49152 

#define FAULT_AD_VALUE 65535


#define CUR_INDEX_NUM     5    //最多支持的档位     增加到  5 个 

//#define MAX_TEMP_OBJCTS_NUM        5//10 modified by jw 2015-06-01


// typedef unsigned char UINT8;
// typedef char INT8;
// typedef unsigned short UINT16;
// typedef short INT16;

typedef  unsigned char UINT8;
typedef  unsigned short UINT16;
typedef  unsigned int UINT32;

typedef unsigned int UINT32;
typedef int INT32;
typedef float FLOAT32;
typedef double FLOAT64;


// PALLETE TRAN OBJ 

typedef struct 
{
	char aName[4];
	char aMember1[4];
	char aMember2[4];
	unsigned short type;
	unsigned short way;
	
}unionObjPara_s; // cl  OBJECT SEND SERIAL 

typedef struct{
	char  info[1000];
}uobjInfo_s;

typedef union{

	uobjInfo_s unusedInfo;
	char  PaletteArray[256 * 4];
}paletteOrUobj_u;


typedef enum objectType_s {
	OBJECT_TYPE_NONE = 0,
	OBJECT_TYPE_RECT = 1,
	OBJECT_TYPE_SPOT = 2,
	OBJECT_TYPE_LINE = 3,
	OBJECT_TYPE_ELLIPSE = 4,
	OBJECT_TYPE_POLYGEN = 5,
} OBJECT_TYPE;


//测温目标 温度信息集合的单元结构体  改为CHAR *指针类型 


typedef struct tagPointMe {
    INT16 x;
    INT16 y;
} POINTME, *PPOINTME;

typedef struct tagRectMe {
    INT16 left;
    INT16 top;
    INT16 right;
    INT16 bottom;
} RECTME, *PRECTME;

typedef struct OBJ_INFO {
    char name[4];
    union
    {
        RECTME m_rect;//
        POINTME m_point;
        //LINE line;
    };
    short emiss;
    short alarm_max_temp_10; // *10         报警用的
    short alarm_min_temp_10; // *10 
    short type;
} obj_info_;      // FOR CL MACHINE TEMP 



#define  VERSION_MAIN       1
#define  VERSION_LOW_NEW    6  // 2017-4-22
// VERSION LOW  5 , IS BEFORE 2017-4-22

//#pragma pack(push, 1)

typedef	struct tagTRAWFileHeader 
{
	WORD		Version; 			//版本号 FROM GUIDE IR
	WORD		VersionLow;			

	DWORD		LanguageID;			//语言

	DWORD		IRBlockOffset; 		//红外图像数据块偏移地址 1 WORD PARALEN  ,.... PARA ..... IMG .....
	DWORD		IRBlockLength; 		//红外图像数据块长度

	DWORD		VLBlockOffset; 		//可见光图像数据块偏移地址
	DWORD		VLBlockLength; 		//可见光图像数据块长度

	DWORD		AudioBlockOffset; 	//语音数据块偏移地址
	DWORD		AudioBlockLength; 	//语音数据块长度

	DWORD		AnalysisBlockOffset; 	//分析数据块偏移地址
	DWORD		AnalysisBlockLength; 	//分析数据块长度

	DWORD		TextBlockOffset;		//文本注释块偏移地址
	DWORD		TextBlockLenght;		//文本注释块长度

	DWORD		ReservedLength;			//保留字节大小
	DWORD		Reserved[3];

}	TRAWFILEHEADER,*LPTRAWFILEHEADER;



typedef	struct tagVLParameterBlock
{
	WORD	ImageWidth;	 	//图像宽度
	WORD	ImageHeight; 	//图像高度
	WORD	dwFormat;
}  VLParameterBlock,*LPVLParameterBlock;

typedef	struct tagAudioBlock
{
	WORD	dwStereo;
	WORD	SampleRate;	 	//采样率
	WORD	SampleBit;	 	//采样精度
	DWORD	Length; 		//采样长度
}  AudioBlock,*LPAudioBlock;


//2010-7-20

typedef struct tagVLVideoPara{ 
	BYTE byBrighness;	
	BYTE byContrast;	
	BYTE byHue; 
	BYTE bySaturation;	
	BYTE byDefBrighness;	
	BYTE byDefContrast;	
	BYTE byDefHue; 
	BYTE byDefSaturation;	
}VLVideoPara;		//可见光视频参数


// 下面 结构 是 没有单字节对齐的 

typedef struct tagTVideoScopeHeader
{	//TOTAL:64bytes
	char	sType[10];			//10 
	char	sStartTime[20];		//20
	char	sEndTime[20];		//20
	char    nomean[2];
	DWORD	totalFrame;//帧数	//4
	DWORD	dwTimes;//录像时间	//4
	short   imgwid;
	short   imghei; //   数据的宽 高 
}	TVIDEOSCOPEHEAD,*LPTVIDEOSCOPEHEAD;

//#pragma pack(pop)






//#pragma pack(push, 4)
//----------------------------obj-------------------------
typedef enum OBJECT_STATE_S {
	OBJ_STATE_DEACTIVE = 0,
	OBJ_STATE_LEFT,
	OBJ_STATE_RIGHT,
	OBJ_STATE_TOP,
	OBJ_STATE_TOP_LEFT,
	OBJ_STATE_TOP_RIGHT,
	OBJ_STATE_BOTTOM,
	OBJ_STATE_BOTTON_LEFT,
	OBJ_STATE_BOTTOM_RIGHT,
	OBJ_STATE_MOVE,
	OBJ_STATE_ACTIVE
} OBJECT_STATE;

typedef struct DevRefArea_t {
	short bUseRefArea;
	short RefAreaUpX;
	short RefAreaUpY;
	short RefAreaDownX;
	short RefAreaDownY;
	short RefAreaTemp;
	short RefAreaAD;
} DevRefArea;


// 覆盖 报警的 测温对象信息 ； 
typedef struct rect_obj {

	INT16 mMaxAD; //最大AD
	INT16 mMinAD; //最小AD
	INT16 mAvgAD; //平均AD

	POINTME mPtMax; //最大点坐标
	POINTME mPtMin;
	union
	{
		RECTME m_rect;
		POINTME m_point;
	};
	OBJECT_TYPE ID;
	char  mDesp[4]; // old is 5 
	FLOAT32 mAvgTemp;
	FLOAT32 mMaxTemp;
	FLOAT32 mMinTemp;
	INT16 emiss;
//	INT16 m_nCurSelect;
// 	FLOAT32 alarm_max;
// 	FLOAT32 alarm_min;
// 
// 	char check_alarm_T_cnt;
// 	char check_alarm_L_cnt;
// 	int  alarm_time;
// 	int  remove_time;
} RECT_OBJ, *PRECT_OBJ,OBJ_ALL_INFO;

typedef struct _OBJ_INFO_ {

	INT8 mAlarmType; //报警类型
	POINTME mPtMax; //最大点坐标
	POINTME mPtMin;
	FLOAT32 mAlarmTemp; //报警温度
	RECTME m_rect;
	char mDesp[4];

} obj_info;

//温漂采集参数集合
typedef struct tagSamplePara {
	int start_time; //开始时间
	int total_time; //采样总的时间小时为单位
	int interval_time; //采集时间间隔  秒为单位
	int sample_num; //采样点的总数  实时的去记录
	int end_time; //结束时间
	int tmp; //采集的黑体温度
} SAMPLE;

//存储温漂拟合公式各项系数
typedef struct tagGradePara {

	float K_F; //K_F
	//	unsigned short K_F;   
	short shutterTemp ; // 生成黑体曲线时候 快门的 标准温度；
	float FixedShutterTemp;   // 探测器温度，或者电压 
	short AddAD;   // 等效黑体修正量  

	// 快门问票 
	short  n; //3次项系数

	// 黑体拟合参数
	float Hexp0; //常数项
	float Hexp1; //常数项
	float Hexp2; //常数项
	short  limitL; 
	short  limitH; 
	float HexpT0; //常数项
	float HexpT1; //常数项
	float HexpT2; //常数项
	short  limitTL;
	short  limitTH; 
	short  resv[4]; //常数项

}GradePara  ;

//温漂采样点
typedef struct tagTempMove {
	int shuttet_temp; //快门温度
	int Ambient_temp; //开机快门温度
	int vtemp; //1978电压
	int board_temp; //电路板的温度
	short AD; //AD值
	short SUB_AD; //AD差值
	short is_use; //当前值是否在拟合中起作用
} TEMP_MOVE;




typedef struct FIT_INFO {
    
    union
    {
        double K_F;//
        double exp0;
    };
    union
    {
        double shutterTemp;//
        double exp1;
    };
    union
    {
		double fixShutterTemp;//  FST 下载 
        double exp2;
    };
    double exp3;
    double exp4;
    
    double exp5;
    double exp6;
    double exp7;
    double exp8;
    
    int gear;//档位
    int n;//拟合次数
} Fit_Info;


typedef enum {
	MEASURE_TYPE_SHUTTER = 0, MEASURE_TYPE_BOLD,
} MEASURETYPE;

typedef enum {
	TEMP_UNIT_CELSIUS = 0, TEMP_UNIT_FAHRENHEIT
} TEMP_UNIT;

typedef enum {
	END_TYPE_SMALL = 1, END_TYPE_BIG
} ENDTYPE;

//--------------



#define DEFAULT_EMISS                   100
#define DEFAULT_HUM                     45
#define DEFAULT_DISTANCE             	18
#define DEFAULT_K_PARAM               	78.338  //2014.8
#define DEFAULT_AD_SCALE        		1.0
#define DEFAULT_SHUTTER_TEMP    		200  // 更改进度
#define DEFAULT_AMBIENT_TEMP    		200
#define DEFAULT_SHUTTER_START_TEMP  	200
#define DEFAULT_CUR_LENGTH              16384//16384  change 2014.8

#define DEFAULT_BLACK_AREA_WID_HEI      20           
#define DEFAULT_BLACK_AREA_CT_X0        80   
#define DEFAULT_BLACK_AREA_CT_Y0        60


#define DEFAULT_PerCentTop_CUT          5
#define DEFAULT_PerCentDown_CUT          5

#define MEASURE_MIN_TEMP        		-2740//-400
#define MEASURE_MAX_TEMP        		10000//5000








typedef struct tagParameterLineHarware {
	unsigned short Version;    // 1
	unsigned short VersionLow; // 6 
	unsigned short ImageWidth;
	unsigned short ImageHeight;
	//unsigned short ParaHeight; // 参数行高度  这个参数只有赋值的使用，没有被调用。 为了添加FPS参数，添加了
	unsigned char ParaHeight; 
	unsigned char Cam_FPS; //CHANGE 2018.1 

	char DetectorID[8];
	char DeviceType[8];   

	unsigned short CurveIndex; //温度档位   温度曲线  色带  1,2,3 ...

	unsigned int   ST_seconds_50X; // 开机时间  FRAME cnt
	short Ambient;        //探测器温度，也指快门温度   // ADDRESS  30.31
	short AtmosphereTemp; //环境温度

	short VTemp;    //探测器管脚电压
	short vtemp_fpa ;// 探测器非成像区域 AD   被PWM 占空比32767.0
	
	short KJ_Ambient;  // 开机环境温度 

	// CHANGE 2018.5.15  以上部分为下位机传递的关键信息。  为了考虑
//	char  Reserved1[16];
//	char  Reserved2[16];
//	char  Reserved3[16];

	//FROM  add 2019.4 
	unsigned int det_int_val;  // 4 +  2 + 1 + 2 = 9   ,PC 48 CHAR
	unsigned short Int_Freq_div; //correction_tempture;
	unsigned char correction_gain;
	//unsigned char reserved[9];
	short    correction_b_ave; //add yzw 2018.10

	unsigned char  frame_type; //0 

	unsigned char  is_win_mode ; //add 2019.4
	unsigned short win_wid;
	unsigned short win_hei; 
	unsigned short win_stx; 
	unsigned short win_sty; 
	
	short  last_correct_vtemp ; //add 2019.5 for lwir
	
    unsigned int real_det_int_val; 
	
    //change 2020.1  for shanghai
	//char  Reserved3[16] ;  //  --88 


}PARAMETERLINEHEAD; //120   BYTE 

typedef struct tagParameterLine {
	unsigned short Version;
	unsigned short VersionLow;
	unsigned short ImageWidth;
	unsigned short ImageHeight;
	//unsigned short ParaHeight; // 参数行高度  这个参数只有赋值的使用，没有被调用。 为了添加FPS参数，添加了
	unsigned char ParaHeight; 
	unsigned char Cam_FPS; //CHANGE 2018.1 

	char DetectorID[8];
	char DeviceType[8];   

	unsigned short CurveIndex; //温度档位   温度曲线  色带  1,2,3 ...

	unsigned int   ST_seconds_50X; // 开机时间  FRAME cnt
	short Ambient;        //探测器温度，也指快门温度   // ADDRESS  30.31
	short AtmosphereTemp; //环境温度

	short VTemp;    //探测器管脚电压
	short vtemp_fpa ;// 探测器非成像区域 AD   被PWM 占空比32767.0
	
	short KJ_Ambient;  // 开机环境温度 

	// CHANGE 2018.5.15  以上部分为下位机传递的关键信息。  为了考虑
//	char  Reserved1[16];
//	char  Reserved2[16];
//	char  Reserved3[16];

	//FROM  add 2019.4 
	unsigned int det_int_val;  // 4 +  2 + 1 + 2 = 9   ,PC 48 CHAR
	unsigned short Int_Freq_div; //correction_tempture;
	unsigned char correction_gain;
	//unsigned char reserved[9];
	short    correction_b_ave; //add yzw 2018.10

	unsigned char  frame_type; //0 

	unsigned char  is_win_mode ; //add 2019.4
	unsigned short win_wid;
	unsigned short win_hei; 
	unsigned short win_stx; 
	unsigned short win_sty; 
	
	short  last_correct_vtemp ; //add 2019.5 for lwir
	
    unsigned int real_det_int_val; 

    //change 2020.1  for shanghai
	char  Reserved3[16] ;  // 88    2020 TO 16 

	unsigned char  M_C;
	unsigned char  M_B;
	short  L_BC_MIN  ;  // OLD IS 24 , SUB   -8  = 16
	short  L_BC_MAX  ;
	short  L_BC_MIN_CUT ;
	short  L_BC_MAX_CUT ;

	// 实时参数  从这里开始，非测温版本的，可以 不用考虑了。 

	//add 2018.5 全手动亮度对比度；
	short    iPole;   // add 2020.1
	short    iCurrBCType;  //2018 增加的量，  0  自动亮度对比度 ， 1  手动亮度对比度  观瞄版本用户， 2  全用户亮度对比度 方法2018.5 ADD 。

	float Contrast;  // temp calc for reg
	float Brightness;
	float K_THR ; 
	short cDicardADPerCentTop;     // 约定为 千分比 的
	short cDicardADPerCentBottom;  // 约定为 千分比 的    -------120 

	
	UINT		m_filterType;  //当前使用的滤波算法  NO .. ADD TEMP USED.   0X7777
	// 用户数据，  PC 用户需要关注的， 考虑
	unsigned short PaletteIndex;


#ifdef  IS_SIGNED_OR_UNSIGNED_DATA
	short iAutoMaxAdValue;   // 实时解算  hist
	short iAutoMinAdValue;
	short nMaxAdValue;
	short nMinAdValue;
	short nCenterAdValue ; //中心点 AD  ADD YZW 
#else 
	unsigned short iAutoMaxAdValue;  // 实时解算  hist
	unsigned short iAutoMinAdValue;
	unsigned short nMaxAdValue;
	unsigned short nMinAdValue;
	unsigned short nCenterAdValue ; //中心点 AD  ADD YZW  需要 ？
	
#endif 

	short maxp_x;  // TEMP USED
	short maxp_y;
	short minp_x;
	short minp_y;
	
	float maxTemp;
	float minTemp;

	float ADScaleX;  // 1.0

	char memo[16];
	char Date[20];

	char GbitNetIpSet[32];  // "192.168.1.124"
	char VL_File_Name[16];
	char Wave_File_Name[16];

	GradePara formula[CUR_INDEX_NUM];  //OLD 96 NEW 56
	char BUFF_REV[40];  //!!!!!

	short CurveLength;   // OLD VER IS 16384 OR 8192 ....


	// 快门温度索引 或者黑体区域索引 
	short mAmbientIndex;
	TEMP_UNIT m_nTempUnit; 

	short TempUnit; //测温单位类型,TEC中复用为m_tecPolicy
	MEASURETYPE	mMeasureType ;  

	//unsigned short K_F;//曲线的斜率
	float K_F;//曲线的斜率
	short Correction_X0; 
	short Correction_X1;
	short KM_Adjust_ADD;

	unsigned short Emiss;
	unsigned short RelHum;
	unsigned short Distance;

	float mCoEfficient;   // 0 

	// 目前支持的  5 个矩形， 5 个 点目标   2019 改为 3 个，  全局一个，黑体一个，  用户一个，
	short obj_cnt;  //  0
	RECT_OBJ obj_info[MAX_TEMP_OBJCTS_NUM];

	// PC 层面需要处理下 
//	short spot_cnt;
//	spot_info_ spot_info[MAX_TEMP_OBJCTS_NUM];

	short bUseRefArea;
	short RefAreaUpX;
	short RefAreaUpY;
	short RefAreaDownX;
	short RefAreaDownY;
	short RefAreaTemp;
	short RefAreaAD;

	short bUseTempPallete;   // 
	char  iISOthermNum;      //  报警温度 色彩 
	char  iISOColorNum;      //
	short TempPalleteUpLimit;  // WHEN T ,  TO  nMaxAdValue ..
	short TempPalleteDownLimit;
	short ISOUP[MAX_ISO_THERM_NUM]; //AD
	short ISODOWN[MAX_ISO_THERM_NUM];
	COLORREF  ISOCOLOR[MAX_ISO_THERM_NUM]; //ADD 2020  20BIT ... 报警颜色 
	short ISOUPT[MAX_ISO_THERM_NUM]; 
	short ISODOWNT[MAX_ISO_THERM_NUM]; //TEMP
	short  mapPts[17] ; //for vl to ir 
	short  bUseMinMax ; //
	short  bUseMask; // alarm mask
	short  bUseRegionGrow; //region arith
	short  RegionIncrease; 
	short  Regionsize; 
	short  Regiondis; 
 
	char Reserved[64]; // 128 DEL ISOCOR mappts. 


	//char  PaletteArray[256 * 4];
#if 1 //cl  change 
	paletteOrUobj_u paletteOrUobj;
#endif
	// 去掉此结构， 考虑不在下面做测温快门采集 图像帧传输出去
	//TEMP_MOVE temp_move[TEMP_MOVE_NUM];

	short CurveData[CURVE_LENGTH]; // 16384  

	// WINDOWS 版本才有的变量  NIOS 没有 
//#ifdef   WIN32   // FOR PC 

	char  smooth_frame_num;  //add 2015.10  添加多帧平滑功能 默认值 0 ； 

	unsigned char  SeriealPort ; // ADD 2018.5 为了 CAMLINK 配套的SERAL 添加的 串口端口号 。 
	int   SP_band ;
	char  SP_parity ;
	int   SP_databits ; 
	int   SP_stopsbits ; 

	unsigned char   cl_cardid; 
	unsigned char   cl_chanid; 
	//char  GbitNetIpSet[32];


	char   IS_USE_M_CARD ; //for gnet for mul; 

//#endif 
	

} PARAMETERLINES, *LPPARAMETERLINES;





//----------------------------------------------------------------


#define    GETB1B2_AVERAGE_FRAME_CNT        1 // 16 

enum VIDEO_TEMP_MEASURE_STATUS
{
	GEN_Y16,
	GEN_X16,
	GET_B1,
	GET_B2_K
};


//--------------------------------------------------------------------
// old gbit use plearo  card ... 

#define	MAX_STRING_LEN			256

typedef struct  _GNET_DEVLIST_
{
	char DevName[255];
	char DevIP[255];
	char DevMAC[255];
	char DevINFO[255];
	BOOL DevEnable;
	// mcard use
    char netmask[255];
    char gateway[255];
    char dns1[255];
    char dns2[255];
	
}GNET_DEVLIST, MNET_DEVLIST;

//消息结构
#define WM_NETCARD_GETCMD		(WM_USER + 0x5050)
typedef struct _tagGNET_CMD_
{
    unsigned char lData[MAX_STRING_LEN];
	unsigned int lSize; 
}GNET_COMMAND;

typedef int (WINAPI* MessageFilter)(void *pUserData, unsigned short messageID, unsigned char *pData, unsigned int length);



extern "C" { 
//设备操作     
//按照IP地址打开设备  窗口句柄用来反馈消息
int  DLLPORT GBitnetSearch(GNET_DEVLIST *m_Gnet_card_list);   //网络相机搜索函数
int  DLLPORT IR_GnetOpen(HWND hwnd, char *IPAddr,int bGrab=0,int packetsize=1440, int skip=0);


//	输入参数：	
//	hwnd：		消息处理窗口句柄
//	IPAddr：	仪器IP地址    格式为[192.168.1.22]
//	bGrab       数据接收可以采用连续接收和用户主动捕捉模式，回调函数只能在bGrab=0 即连续接收模式下使用
//  packetsize  图像数据传输时候每个包的大小  必须是 32 的倍数 
//	skip        连续采集模式下采集的间隔
//	返回值：
//	> 0 连接到仪器后的操作句柄
//	<= 0 连接失败
BOOL DLLPORT IR_SetGnetStreamCapInterval(int handle, int skipcnt);   // 百兆网和千兆网通用 
int  DLLPORT IR_GetGnetStreamCapInterval(int handle);  


};

//-------------------------------------------------------------------------------------


const short MAX_SIGCHARBUFFER	=	255;

//added by jw 2017-05-17
#define DEVICE_MODEL       ("G003L")
#define DETECTOR_TYPE	    ("MT6415")
#define DETECTOR_SERIAL_NUM		("00000001")

//added by jw 2017-04-09
//configuration register
#define	AVALON_DET_DEFAULT_CONFIG_VALUE			(0x8ba00087)
//integration time register
#define	AVALON_DET_DEFAULT_INT_TIME_VALUE			(1000)
#define	AVALON_DET_DEFAULT_INT_TIME_MIN			(1)
#define	AVALON_DET_DEFAULT_INT_TIME_MAX			(217310)

#define AVALON_DET_CONFIG_VALUE         (AVALON_DET_DEFAULT_CONFIG_VALUE)
#define AVALON_DET_INT_TIME_VALUE       (AVALON_DET_DEFAULT_INT_TIME_VALUE)
#define AVALON_DET_INT_TIME_MIN         (AVALON_DET_DEFAULT_INT_TIME_MIN)
#define AVALON_DET_INT_TIME_MAX         (AVALON_DET_DEFAULT_INT_TIME_MAX)




//VSK电压目标值5.12V，数值3900，电路放大系数为1.243
//GFID电压目标值3.00V，数值2900，电路无放大
#define I2C_AD5339_VDETCOM_DIGIT	(2250)//(3900)
#define I2C_AD5339_VREF_DIGIT		(2700)//(2900)
#define I2C_AD5339_VSK_DIGIT		(I2C_AD5339_VDETCOM_DIGIT)
#define I2C_AD5339_GFID_DIGIT		(I2C_AD5339_VREF_DIGIT)
//VBUS电压目标值2.80V,对应数值2680，目前电路上拉到2.771V
//GSK电压目标值2.12V，对应数值2050，目前电路上拉到2.109V
#define	I2C_AD5339_VBUS_DIGIT		(2680)
#define	I2C_AD5339_GSK_DIGIT		(2050)

#define	BIAS_VSK_DIGIT				(I2C_AD5339_VSK_DIGIT)
#define	BIAS_GFID_DIGIT				(I2C_AD5339_GFID_DIGIT)
#define	BIAS_VBUS_DIGIT				(I2C_AD5339_VBUS_DIGIT)
#define	BIAS_GSK_DIGIT				(I2C_AD5339_GSK_DIGIT)


// 262144  one block
// 64 BLOCK
#define FLASH_MEM_SIZE              (16777216)  //falsh size 16MB=16777216Byte
#define STORAGEBLOCK_NUM            (36)        //16M 一共是  64 个块 ， 使用了 36个块 3+3 + 30


//added by jw 2017-04-09
typedef struct _CONFIG_ARG_ {
	//是否是第一次配置
	short FIRST_CONFIG ;

	//-------------功能参数-----------------------

	//打快门需要延时的帧数默认为5帧 快门打上去
	short SEND_SHUTTER_CNT;
	//快门回来
	short SEND_SHUTTER_BACK_CNT;

	//快门校正需要缓存的帧数默认为8帧
	short CWWAITKM_CNT;

	//机芯稳定后个多长时间打一次快门默认为300秒 
	short SENDSHUTTER_TIME;     //

	//自动打快门 
	short SENDSHUTTER_AUTO_MODE;  // -1  开机打一次， 0  始终不打，  1  自动打 按照 SENDSHUTTER_TIME 节拍。

	// 2019.12 for sync mode
	short SYNC_MODE;  // SYS_REV0;

	//亮度对比度帧平滑的数量默认为8
	short SMOOTH_FRAME_CNT;

	//手动调节对比度的步长默认24
//	short BLACKBODY_WID;
	short NOUSED0;
	//手动调节亮度步长默认 12
	short NOUSED1;


	//顶部底部抛点数量
	short NOUSED3; //  HIST_CUT_CNT;
	//自动亮度对比度状态下的对比度上限值默认为2048
	short NOUSED4 ; //  AUTO_CON_LIMIT_UP;
	//手动状态下对比度上限
	//short MANUAL_CON_LIMIT_UP;  // CHANGE 2018.10
	short   Image_ave; //

	//---------------------------1979控制------------
	// 2016.3 改动， 去掉原来  TEMP_1979_LOW_LIMIT TEMP_1979_HIGH_LIMIT 
	short START_1979_UP_VALUE;    // 开机温度 或者上次开机温度，用作测温使用。  
	//short Int_Resv0;   //积分时间预留  

	// 改做别的应用    但位置不变，保持原来的数据结构。 
	// 自动积分时间 的 相关参数，留给后面

	short AutoInt_POLICY;      // 是否采用自动爆光  0 ，不采用， 1 采用 
	// // 自动曝光 目标AD 平衡点 。
	short AutoIntDestAd;         



	//1979工作温度点
	short WORK_1979_TEMP;

	//温控策略
	short CT_POLICY ;

	// ADD YZW 偏压设置 
	unsigned short VSK;  // 一般为 
	unsigned short GFID; // 一般为 
	unsigned short VBUS; //2.8   25mv
	unsigned short GSK;  //2.12  50mv

	// ADD 2016.3  PID 
	unsigned  short Kp; 
	unsigned  short Ki; 
	unsigned  short Kd; 

	//modified by jw 2018-05-25
	//adc clok phase shift object:unit is ps.
	 int phase_object;//SYS_REV1 ;  // change to int  unsigned .  

	short FlashValidPage;

	//以下为  探测器广联 的
	 //积分时间倍数（实际是帧频分频数，n=1,2,4,8...,2^N.）
	unsigned short  Int_Freq_div;

	//	unsigned int SENSOR_SERIAL_DATA;
	//探测器积分时间可能以微秒或者探测器工作时钟周期数
	//根据不同探测器确定，目前最大不超过24位
	unsigned int Int_time;

	//不同类型探测器的串口配置数据（位数和内容）不同
	//如果超过32位时根据具体需求重新编组成32位
	// 增益-翻转-内部偏压-通道
	//  2   - 3 - 12  -- 3 ,
	unsigned int SENSOR_SERIAL_DATA0;  //

	//modified by jw 2017-05-17
	//min integral time
	unsigned int SENSOR_SERIAL_DATA1;
	//max integral time
	unsigned int SENSOR_SERIAL_DATA2;
	//detector type name,such as "ISC0002"
	char detector_type[16];
	//detector serial num, such as "12345678"
	char detector_serial_num[16];
	//device model name,such as "G003L"
	char device_model[16];
	//device communication interface type name,such as "IRUSBFT"
	char device_comm_if_type0[16];
	char device_comm_if_type1[16];
	
	//
	unsigned short hardware_version;
	unsigned short software_version;
	//the time of latest software revision
	//[31:20]~year,[19:16]~month,[15:11]~day,
	//[10:6]~hour,[5:0]~minute
	unsigned int hardware_revision_time;
	//the time of latest software revision
	//[31:20]~year,[19:16]~month,[15:11]~day,
	//[10:6]~hour,[5:0]~minute
	unsigned int software_revision_time;

//	unsigned int det_int_val[10];
	//ADD YZW 2018.7
	int     resv_2018 ;  //V1V2 版本为    phase_object BUT  NEW 2018.10 CORE USE UP..
	// ARITH or para ;  add 2018.12 
	short   col_arith_type;
	short   col_add[8];

	unsigned short FRAME_SKIP_CNT;


} CONFIG , *pCONFIG;

//#pragma pack(pop)

//-------------------------------------------------------------------------


//-------------------------------------------------------------------------

extern "C"
{
	//一部分内部功能使用的。 
	
	int DLLPORT  IR_GetLostFrameCnt(void * handle); // for test 
    BOOL DLLPORT IR_EnableSaveBP(void * handle, int mode);
	
	// 内部使用  
    BOOL DLLPORT  IR_DebugSet(void * handle,BOOL set);	        
	void DLLPORT  IR_DebugGetPara(void * handle,short xishu[10]);  
	BOOL DLLPORT  IR_DebugSetPara(void * handle,short xishu[10]);  
	// 算法使用  
	BOOL DLLPORT  IR_SetArithType(void * handle, int type);  
	int  DLLPORT  IR_GetCurrArithType(void * handle);  
	
	
	// 2014 增加坏点接口 
    short   DLLPORT  * IR_GetDevieceBpImage(void * handle);
    void    DLLPORT   IR_SetDevieceBpImage(void * handle,short * image);  //SDK层面的坏点信息； 
	
	
	//  下位机关于时间的问题， 
	
	
	//   int   DLLPORT IR_SetSysConfigPara(int handle,void * para); 
	
	void  DLLPORT time_init(void);
	
	int   DLLPORT get_time_begin(void);
	int   DLLPORT get_time_end(void);
	int   DLLPORT get_time_span(void);
	void  DLLPORT time_delay(int milli_seconds);

};






#endif 
