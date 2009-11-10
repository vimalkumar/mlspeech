# Handy script to try out combinations of test and training inputs


PROJ_HOME=..

function run {
    train=$1
    test=$2

    trian_all=""
    for i in $train
    do
	train_all="$train_all `echo $PROJ_HOME/data/$i/*.wav`"
    done

    test_all=""
    for j in $test
    do
	test_all="${test_all} `echo $PROJ_HOME/data/$j/*wav`"
    done
#    set -x
    result=`$PROJ_HOME/src/run.py /tmp/t.tmp --train $train_all --test $test_all  | grep Accuracy`
#    set +x
    echo "|$train|$test|$result|"
}

run "vimal srinath" melchi
run "vimal melchi" srinath
run "srinath melchi" vimal
run vimal srinath
run srinath vimal
