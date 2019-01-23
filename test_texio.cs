using System;
using Vector.Tools;
using Vector.CANoe.Runtime;
using Vector.CANoe.Sockets;
using Vector.CANoe.Threading;
using Vector.Diagnostics;
using Vector.Scripting.UI;
using Vector.CANoe.TFS;
using Vector.CANoe.VTS;

// 注意： 
// - DBCファイルから周期監視用XML/CAPLテストモジュールが自動生成できる
// - DLC CheckクラスはDBCファイルがないと利用できない。
// 
// 備考：
// DBCファイルからDLC監視用XML/CAPLテストモジュールが自動生成できる
// CANoeのHelp(.chm)
// Test → Basics → Function Overview → Generation Test Modules
// → Testing Interaction Layer parameters from CANdb++ を参照

public class test_texio : TestModule
{
    public override void Main()
    {
        // ここに、[TestCase()]アトリビュートをつけたテストに記載していく。

        TestGroupBegin("basic", "cyclic, dlc"); // <-- test_texio→basic→Cycle Time checkという階層になる。
        TC_CycleTimeCheck(1000);
        TC_DlcCheck(1000);
        TestGroupEnd();
    }

    [TestCase("Cycle Time Check", "Check of cycle time")]
    public void TC_CycleTimeCheck(int nTime)
    {
        // レポート出力
        Report.TestCaseTitle("Cycle Time Check");
        Report.TestCaseComment("Test pattern begin");
        
        // 監視開始
        CANFrame frame1 = new CANFrame(0x123, 8);
        CANFrame frame2 = new CANFrame(0x321, 8);

        ICheck check1 = new AbsoluteCycleTimeCheck<CANFrame>(frame1, CheckType.Condition, 90, 110);
        ICheck check2 = new AbsoluteCycleTimeCheck<CANFrame>(frame2, CheckType.Condition, 190, 210);

        check1.Activate();
        check2.Activate();

        // 指定時間待ち
        Execution.Wait(nTime);

        // 監視完了
        check1.Deactivate();
        check2.Deactivate();
        check1.Dispose();
        check2.Dispose();

        // レポート出力
        Report.TestCaseComment("Test pattern end");
    }

    [TestCase("DLC Check", "Check of DLC")]
    public void TC_DlcCheck(int nTime)
    {
        // レポート出力
        Report.TestCaseTitle("DLC Check");
        Report.TestCaseComment("Test pattern begin");

        // 監視開始
        ICheck check1 = new DlcCheck<NetworkDB.Frames.ControlMsg>(CheckType.Condition);
        check1.Activate();

        // 指定時間待ち
        Execution.Wait(nTime);

        // 監視完了
        check1.Deactivate();
        check1.Dispose();

        // レポート出力
        Report.TestCaseComment("Test pattern end");
    }


}

/* 
# AbsoluteCycleTimeCheck<T> Constructor (IFrame, CheckType, Int32, Int32) 

The constructor for an AbsoluteCycleTimeCheck. 

Namespace:  Vector.CANoe.TFS
Assembly:  Vector.CANoe.TFS.dll
Syntax


```C#
public AbsoluteCycleTimeCheck(
	IFrame frame,
	CheckType type,
	int minAbsoluteCycleTime,
	int maxAbsoluteCycleTime
)
```

## Parameters
frame   Type: IFrame
  The CAN frame object for which the check is applied.

type  Type: Vector.CANoe.TFS.CheckType
  The check type can be 'Condition', 'Constraint' or 'Observation'. 

minAbsoluteCycleTime  Type: System.Int32
  A violation is detected if minAbsoluteCycleTime (in milliseconds) is under-run.

maxAbsoluteCycleTime  Type: System.Int32
  A violation is detected if maxAbsoluteCycleTime (in milliseconds) is exceeded.

====
# public enum CheckType

The type of a check. The default type is Condition. 

## Members
 Constraint   0 Constraints are used to monitor the test setup and the test environment.  
 Condition    1 Conditions are used to check the system to be tested during the test procedure.  
 Observation  2 Observations are used to check conditions or constraints that should not lead to a fail of the test module/test unit on violation.  
====

# Execution.Wait Method (Int32) 

Waits a certain timespan. During the wait, the measurement and simulation are not blocked. 

Namespace:  Vector.CANoe.Threading
Assembly:  Vector.CANoe.Threading.dll

```C#
Copypublic static int Wait(
	int timeSpan
)
```
## Parameters
timeSpan Type: System.Int32
  duration of the wait, in milliseconds

Return Value
  Type: Int32

WAIT_TIMEOUT: if the given timespan elapsed
WAIT_ABORTED: if the measurement was stopped before the given timespan elapsed
WAIT_NOT_ALLOWED: if wait was called from non-Test, -Snippet or -Waiting Handler code

Exceptions
 */