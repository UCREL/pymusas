import Admonition from '@theme/Admonition';
import ThumbsUpSVG from '@site/static/thumbs-up.svg';
import ThumbsDownSVG from '@site/static/thumbs-down.svg';

export function PositiveArea({children}) {
  return (
    <div>
      <Admonition type="tip" icon={<ThumbsUpSVG/>} title="Advantages">
        {children}
      </Admonition>
    </div>
  );
}

export function NegativeArea({children}) {
  return (
    <div>
      <Admonition type="danger" icon={<ThumbsDownSVG/>} title="Drawbacks">
        {children}
      </Admonition>
    </div>
  );
}
