/**
 * AutoGen
 */
public class SM_PlayerInfo{

    /** id */
    public var id:int;

    /** 名字 */
    public var name:String;//测试

    /**
     * 年龄
     */
    public var age:int;

    /** 钱 */
    public var money:long;

    /** 布尔 */
    public var isAuto:Boolean;

    public var aSimpleMap:Object;

    /** a list */
    public var aSimpleList:List<LevelChangeAndExp>;

		override protected function reading():Boolean {
			id = readInt();
			name = readString();
			age = readInt();
			money = readLong();
			isAuto = readBoolean();
			aSimpleMap = readObject();
			aSimpleList = readObject();
			return true;
		}

}
